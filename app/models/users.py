from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion

from app.db.base_class import Base

force_auto_coercion()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(EmailType(50), unique=True, nullable=False)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)
