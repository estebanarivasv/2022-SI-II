from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Flask API RESTFUL principal initialization
api = Api()

# Database principal initialization
db = SQLAlchemy()

# Authentication handler principal initialization
jwt = JWTManager()
