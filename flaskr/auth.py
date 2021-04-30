import functools
import bcrypt

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from flaskr import database
from flaskr.models import user

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.json['username'].encode('utf-8')
    email = request.json['email'].encode('utf-8')
    password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())
    error = None

    if not username:
      error = 'Username is required.'
    elif not email:
      error = 'Email is required.'
    elif not password:
      error = 'Password is required.'
    elif user.User.query.filter_by(email=email).first() is not None:
      error = f'Email {email} is already used.'.format(username)

    if error is None:
      user_register = user.User(username=username, email=email, password=password, role=1)
      
      try:
        database.session.add(user_register)
        database.session.commit()
        return jsonify(
          status="success",
          message="Registered successfully !"
        )
      except IntegrityError as e:
        error='Email is already used.'
        database.session.rollback()

    flash(error)

    return jsonify(
      status="error", 
      message=error
    )

@bp.route('/login', methods=('GET', 'POST'))
def login():
  if request.method == 'POST':
    email = request.json['email'].encode('utf-8')
    password = request.json['password'].encode('utf-8')
    user_login = user.User.query.filter_by(email=email).first()
    hash_pass = user_login.password.encode('utf-8')
    error = None

    if user_login is None:
      error = 'Incorrect email.'
    elif not bcrypt.checkpw(password, hash_pass):
      error = 'Incorrect password.'

    if error is None:
      session.clear()
      session['user_id'] = user_login.id
      return str(session['user_id'])

    flash(error)

    return jsonify(
      status="error", 
      message=error
    )