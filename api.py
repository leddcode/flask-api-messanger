from datetime import timedelta
import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_jwt import JWT
from flask_restful import Api

from database import engine
import models
from resources.messages import (
    AllMessages, Message, NewMessage, UnreadMessages)
from resources.user import Register
from security import authenticate, identity

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
app.secret_key = os.getenv('SECRET')
jwt = JWT(app, authenticate, identity)
api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(AllMessages, '/received')
api.add_resource(UnreadMessages, '/unread')
api.add_resource(NewMessage, '/send_message')
api.add_resource(Message, '/message/<int:message_id>')


@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=False)
