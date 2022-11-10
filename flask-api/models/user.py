from datetime import datetime

from db import db
from passlib.hash import pbkdf2_sha256 as sha256


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    text = db.Column(db.String(1000))
    sender = db.Column(db.String(80))
    receiver = db.Column(db.String(80))

    def __init__(self, text, sender, receiver):
        self.text = text
        self.sender = sender
        self.receiver = receiver
        self.date = datetime.now()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def find_by_receiver(receiver):
        return Message.query.filter_by(receiver=receiver).all()

    def json(self):
        return {
            'id': self.id,
            'date': self.date,
            'text': self.text,
            'sender': self.sender,
            'receiver': self.receiver
        }


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    public_key = db.Column(db.String(240), unique=True, index=True, nullable=False)
    private_key = db.Column(db.String(240), unique=True, index=True, nullable=False)
    rsa_key = db.Column(db.String(240), unique=True, index=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
