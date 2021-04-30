import functools
import bcrypt

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from flaskr import database
from flaskr.models import user
from flaskr.helpers import json_response

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  if request.method == 'POST':
    username = request.json['username']
    email = request.json['email']
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
