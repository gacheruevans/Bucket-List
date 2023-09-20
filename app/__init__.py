from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name):
    """
    This function creates a Flask instance for
    the application and configures it.
    """
    app = Flask(__name__)
    
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    app.config.from_object(config[config_name])

    db.init_app(app)

    return app


app = create_app('development')
