from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, fields, marshal_with, reqparse

from crud import (
    create_message,
    delete_message,
    get_message,
    get_received_messages,
    get_user_by_id
)
from database import get_db
from models import MessageModel

serialize_fields = {
    'id': fields.Integer,
    'sender': fields.Integer,
    'receiver': fields.Integer,
    'subject': fields.String,
    'content': fields.String,
    'creation_date': fields.DateTime,
    'is_unread': fields.Boolean
}


@marshal_with(serialize_fields)
def render_object(object):
    return object


class AllMessages(Resource):
    @jwt_required()
    def get(self):
        db = next(get_db())
        messages = get_received_messages(db, current_identity.id)
        if messages:
            return render_object(messages)
        return {'message': 'There are no messages!'}


class UnreadMessages(Resource):
    @jwt_required()
    def get(self):
        db = next(get_db())
        messages = get_received_messages(db, current_identity.id)
        unread = [mes for mes in messages if mes.is_unread]
        if unread:
            return render_object(unread)
        return {'message': 'There are no unread messages!'}


class Message(Resource):
    @jwt_required()
    def get(self, message_id):
        db = next(get_db())
        message = get_message(db, message_id)

        if not message:
            return {"message": "The message doesn't exist!"}, 404

        if current_identity.id not in (message.sender, message.receiver):
            return {"message": "You are not able to read the message!"}, 500

        if message.receiver == current_identity.id:
            message.is_unread = False
            db.commit()
        return render_object(message)

    @jwt_required()
    def delete(self, message_id):
        db = next(get_db())
        message = get_message(db, message_id)

        if not message:
            return {"message": "The message doesn't exist!"}, 404

        if current_identity.id not in (message.sender, message.receiver):
            return {"message": "You are not able to delete the message!"}, 500

        delete_message(db, message)
        return {'message': 'The message was successfully deleted.'}


class NewMessage(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'receiver',
        type=int,
        required=True,
        help="Every message has a receiver."
    )
    parser.add_argument(
        'subject',
        type=str,
        required=True,
        help="Every message has a subject."
    )
    parser.add_argument(
        'content',
        type=str,
        required=True,
        help="Every message has a content."
    )

    @jwt_required()
    def post(self):
        db = next(get_db())
        sender = current_identity.id
        data = NewMessage.parser.parse_args()
        error_message = self._validate_request(db, data['receiver'], sender)
        if error_message:
            return {"message": error_message}, 500
        try:
            new_message = MessageModel(
                sender=sender,
                receiver=data['receiver'],
                subject=data['subject'],
                content=data['content'],
                owner_id=sender
            )
            create_message(db, new_message)
            return {"message": "The message was successfully sent."}, 201
        except Exception:
            resp = "An error occurred while sending the message."
            return {"message": resp}, 500

    def _validate_request(self, db, receiver, sender):
        if receiver == sender:
            return "The user is not able to send message to himself."

        if not get_user_by_id(db, receiver):
            return "The receiver doesn't exist!."
