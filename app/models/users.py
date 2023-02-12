import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion

from app.db.base_class import Base

force_auto_coercion()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(EmailType(50), unique=True, nullable=False)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)

    keys = relationship(
        "UserKeys",
        back_populates="user",
        lazy='dynamic',
        cascade="all, delete-orphan",
    )
    tokens = relationship(
        "UserToken",
        back_populates="user",
        lazy='dynamic',
        cascade="all, delete-orphan",
    )


class UserKeys(Base):
    __tablename__ = "user_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False
    )
    public_key = Column(String(2000), nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="keys")


class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False
    )
    token = Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    )
    expires = Column(DateTime)

    user = relationship("User", back_populates="tokens", lazy='joined')
