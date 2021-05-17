from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


def reset_database():
    from api.v1.database.user import User
    database.drop_all()
    database.create_all()
