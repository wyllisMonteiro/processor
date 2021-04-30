import bcrypt
import jwt

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from functools import wraps
from flaskr import database
from flaskr.models import user

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    
    if not token:
      return jsonify({'message' : 'Token is missing !!'}), 401

    try:
      data = jwt.decode(token, "dev", "HS256")
      current_user = user.User.query\
        .filter_by(id = data['id'])\
        .first()
    except:
      return jsonify({
        "status": "error",
        "message": "Token is invalid !!"
      }), 401

    return  f(current_user, *args, **kwargs)
  
  return decorated

@bp.route('/check_token', methods=['GET'])
@token_required
def check_token(current_user):
  return "Valid token !!"

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
    status = 200

    if user_login is None:
      error = 'Incorrect email.'
      status = 404
    elif not bcrypt.checkpw(password, hash_pass):
      error = 'Incorrect password.'
      status = 404

    if error is None:
      token = jwt.encode({
        'id': user_login.id,
        'exp' : datetime.utcnow() + timedelta(minutes = 30)
      }, "dev", "HS256")

      return make_response(jsonify(
        status="success", 
      ), status, {"Authorization": token })

    flash(error)

    return make_response(jsonify(
      status="error", 
      message=error
    ), status)
