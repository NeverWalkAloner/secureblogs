"""Celery tasks."""

import os

from celery import Celery
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from sqlalchemy import select, update

from app.core.crypto_tools import (
    asymmetric_encryption,
    generate_symmetric_key,
    symmetric_encryption,
)
from app.db.base import Post, PostKeys, User, UserGroup, UserKeys
from app.db.session import SyncSessionLocal


celery = Celery("secureblogs")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")


@celery.task(name="encrypt_post_content")
def encrypt_post_content(post_id: int, content: str):
    key = generate_symmetric_key()
    encrypted_content = symmetric_encryption(content, key)
    with SyncSessionLocal() as db:
        # update post instance
        post_statement = (
            update(Post)
            .returning(Post.group_id)
            .where(Post.id == post_id)
            .values(content=encrypted_content)
        )
        post = db.execute(post_statement).fetchone()

        # fetch user's public keys from DB
        users_subquery = (
            select(User.id)
            .where(User.groups.any(UserGroup.id.in_([post.group_id])))
            .subquery()
        )
        statement = select(UserKeys).where(
            (UserKeys.user_id.in_(users_subquery))
            & (UserKeys.is_revoked == False)
        )
        public_keys = db.execute(statement).scalars().all()
        db_post_keys = []
        for public_key in public_keys:
            # Save generated keys in DB
            public_pem_data = public_key.public_key
            public_key_object = load_pem_public_key(public_pem_data.encode())
            encrypted_key = asymmetric_encryption(key, public_key_object)
            db_post_keys.append(
                PostKeys(
                    post_id=post_id,
                    public_key_id=public_key.id,
                    encrypted_key=encrypted_key,
                )
            )
        db.bulk_save_objects(db_post_keys)
        db.commit()
