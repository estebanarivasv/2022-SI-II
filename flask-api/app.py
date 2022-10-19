import os
from main import create_app, db


if __name__ == '__main__':
    # Creating Flask app instance
    app = create_app()

    # Loading app context
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=os.getenv('PORT'))  # Set to false because it was creating multiple threads
