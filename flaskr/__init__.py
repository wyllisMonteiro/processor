import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

database = SQLAlchemy()

load_dotenv()

def create_app(test_config=None):
    username_db = os.getenv("MYSQL_USER")
    pass_db = os.getenv("MYSQL_PASSWORD")
    host_db = os.getenv("DB_HOST")
    name_db = os.getenv("MYSQL_DATABASE")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"mysql://{username_db}:{pass_db}@{host_db}/{name_db}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    database.init_app(app)

    with app.app_context():
        from flaskr.models import user
        database.create_all()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    return app
