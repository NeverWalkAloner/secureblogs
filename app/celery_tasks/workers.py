"""Celery tasks."""

import os

from celery import Celery
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from sqlalchemy import select

from app.core.crypto_tools import asymmetric_encryption, generate_symmetric_key
from app.db.session import SyncSessionLocal
from app.db.base import UserKeys, GroupKeys

celery = Celery("secureblogs")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")


@celery.task(name="create_user_key")
def create_user_key(user_id: int, group_id: int):
    key = generate_symmetric_key()
    with SyncSessionLocal() as db:
        statement = select(UserKeys).where(
            (UserKeys.user_id == user_id) & (UserKeys.is_revoked == False)
        )
        public_key = db.execute(statement).scalars().first()
        public_pem_data = public_key.public_key
        public_key_object = load_pem_public_key(public_pem_data.encode())
        encrypted_key = asymmetric_encryption(key, public_key_object)
        db_group_key = GroupKeys(
            group_id=group_id,
            public_key_id=public_key.id,
            encrypted_key=encrypted_key,
        )
        db.add(db_group_key)
        db.commit()
