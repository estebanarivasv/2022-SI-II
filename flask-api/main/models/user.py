from main.extensions import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100))
    messages = db.relationship("Message", back_populates="user", lazy=True, uselist=False)  # One-to-one relationship

    def __repr__(self):
        return f'<User {self.id} {self.name}'
