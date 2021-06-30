from sqlalchemy.orm import Session

from models import MessageModel, UserModel


def get_sent_messages(db: Session, user_id: int):
    return db.query(MessageModel) \
        .filter(MessageModel.sender == user_id).all()


def get_received_messages(db: Session, user_id: int):
    return db.query(MessageModel) \
        .filter(MessageModel.receiver == user_id).all()


def get_message(db: Session, message_id: int):
    return db.query(MessageModel) \
        .filter(MessageModel.id == message_id).first()


def create_message(db: Session, new_message: MessageModel):
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def delete_message(db: Session, message: MessageModel):
    db.delete(message)
    db.commit()
    return message


def get_user_by_id(db: Session, user_id: str):
    return db.query(UserModel) \
        .filter(UserModel.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel) \
        .filter(UserModel.username == username).first()


def create_user(db: Session, new_user: UserModel):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
