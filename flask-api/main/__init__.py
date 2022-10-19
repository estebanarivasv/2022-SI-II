import os
from flask import Flask
from dotenv import load_dotenv

from main.models import *
from main.extensions import db, api, jwt


# Function that activates primary keys recognition in the SQLite DB
def activate_primary_keys(connection, connection_record):
    connection.execute('pragma foreign_keys=ON')


# Function that creates an instance of the Flask application, summing other complements
def create_app():

    # Flask app initialization
    app = Flask(__name__)

    # Loading environment variables
    load_dotenv()

    db_path = str(os.getenv('SQLALCHEMY_DB_PATH'))
    db_name = str(os.getenv('SQLALCHEMY_DB_NAME'))

    # Creating database
    if not os.path.exists(db_path + db_name):
        # Database doesn't exist -> create it
        if not os.path.exists(db_path):
            os.mkdir(db_path)
        os.mknod(db_path + db_name)

    # Database configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + db_path + db_name

    # Database initialization in Flask app
    db.init_app(app)

    # Defining secret key for encryption and time of expiration of each access token that will be generated
    app.config['JWT_SECRET_KEY'] = str(os.getenv('JWT_SECRET_KEY'))
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    # JWT management initialization in Flask app
    jwt.init_app(app)

    # When the database is "connected in Flask app, the primary keys will activate"
    with app.app_context():
        from sqlalchemy import event
        event.listen(db.engine, 'connect', activate_primary_keys)

    # Final app initialization
    api.init_app(app)

    return app
