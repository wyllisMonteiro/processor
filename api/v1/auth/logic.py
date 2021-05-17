import bcrypt
import jwt

from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from functools import wraps

from api.v1.database import database
from api.v1.database.user import User


def token_required(callback):
    @wraps(callback)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'message': 'Token is missing !!'}, 401

        try:
            data = jwt.decode(token, "dev", "HS256")
            current_user = User.query.filter(User.id == data['id']).one()
        except:
            return {'message': 'Token is missing !!'}, 401

        return callback(current_user, *args, **kwargs)

    return decorated


def register(data):
    username = data['username'].encode('utf-8')
    email = data['email'].encode('utf-8')
    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    error = None
    status = 201

    if not username:
        error = "Username is required."
        status = 404
    elif not email:
        error = "Email is required."
        status = 404
    elif not password:
        error = "Password is required."
        status = 404
    elif User.query.filter_by(email=email).first() is not None:
        error = f"Email {data['email']} is already used."
        status = 500

    if error is None:
        user_register = User(username=username, email=email, password=password, role=1)

        try:
            database.session.add(user_register)
            database.session.commit()

            return "Registered successfully !", status
        except IntegrityError as e:
            error = "Email is already used."
            status = 500
            database.session.rollback()

    return error, status


def login(data):
    error = None
    status = 200

    email = data['email'].encode('utf-8')
    password = data['password'].encode('utf-8')

    if not email:
        error = "Username is required."
        status = 404
    elif not password:
        error = "Email is required."
        status = 404

    user_login = User.query.filter(User.email == email).one()
    hash_pass = user_login.password.encode('utf-8')

    if user_login is None:
        error = 'Incorrect email.'
        status = 404
    elif not bcrypt.checkpw(password, hash_pass):
        error = 'Incorrect password.'
        status = 404

    if error is None:
        token = jwt.encode({
            'id': user_login.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, "dev", "HS256")

        return "", status, token

    return error, status, ""
