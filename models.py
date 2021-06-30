from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    messages = relationship("MessageModel", back_populates="owner")


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, nullable=False)
    receiver = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.today())
    is_unread = Column(Boolean, nullable=False, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="messages")
