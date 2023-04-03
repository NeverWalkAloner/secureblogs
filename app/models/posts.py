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
