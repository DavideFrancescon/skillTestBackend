
# flask imports
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
SECRET_KEY = 'your secret key'

if __name__ == "__main__":
    from blueprints import( auth_blueprint, table_blueprint, users_blueprint)
    from database import base
    from database import session
    from database import db
    base.metadata.create_all(db)
    session.commit()
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(table_blueprint, url_prefix="/api")
    app.register_blueprint(users_blueprint, url_prefix="/api")
    CORS(app)
    app.run(debug=True)
