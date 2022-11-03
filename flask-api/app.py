import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, UserLogout, UserSendMail

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['PROPAGATE_EXCEPTIONS'] = os.getenv("PROPAGATE_EXCEPTIONS")
app.config['JWT_BLACKLIST_ENABLED'] = os.getenv("JWT_BLACKLIST_ENABLED")
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = os.getenv("JWT_BLACKLIST_TOKEN_CHECKS")
app.secret_key = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required.'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_headers, jwt_payload):
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required.'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked.'
    }), 401


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(User, '/profile')
api.add_resource(UserSendMail, '/sendmail')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=os.getenv("PORT"), debug=True)
