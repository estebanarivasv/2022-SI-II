from db import db


class Message(db.Model):
    __tablename__ = "Message"

    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    date = db.Column(db.DateTime(timezone=True))
    text = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('User.id'))  # One-to-one relationship
    author = db.relationship("User", back_populates="messages")
    recipient_id = db.Column(db.Integer, db.ForeignKey('User.id'))  # One-to-one relationship
    recipient = db.relationship("User", back_populates="messages")

    def __repr__(self):
        return f'<Comments {self.id} {self.text}'

    def __init__(self, text, user_id, book_id):
        self.text = text
        self.user_id = user_id
        self.book_id = book_id
