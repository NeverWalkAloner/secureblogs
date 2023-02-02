from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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

    keys = relationship("UserKeys", back_populates="user", lazy='dynamic')


class UserKeys(Base):
    __tablename__ = "user_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    public_key = Column(String(2000), nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="keys")
