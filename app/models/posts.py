from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False
    )
    group_id = Column(
        Integer,
        ForeignKey("user_groups.id", ondelete='CASCADE'),
        nullable=False,
    )

    author = relationship("User", back_populates="posts")
    user_group = relationship("UserGroup", back_populates="posts")
    keys = relationship("PostKeys", back_populates="post")


class PostKeys(Base):
    __tablename__ = "post_keys"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete='CASCADE'),
        nullable=False,
    )
    public_key_id = Column(
        Integer, ForeignKey("user_keys.id", ondelete='CASCADE'), nullable=False
    )
    encrypted_key = Column(Text)

    post = relationship("Post", back_populates="keys")
    public_key = relationship("UserKeys")
