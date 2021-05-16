import logging

from flask import request

from flask_restx import Resource
from api.v1.auth.logic import token_required, register, login
from api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='Operations related to authentification')

@ns.route('/check_token')
class CheckItem(Resource):

  @staticmethod
  @token_required
  def get(current_user):
    return "Valid token !!"

@ns.route('/register')
@api.response(404, 'Authentification failed.')
class RegisterItem(Resource):

  #@api.marshal_with(category_with_posts)
  @staticmethod
  def post():
    """
    Returns message success | error
    """
    message, status = register(request.json)
    return { "message": message }, status

@ns.route('/login')
@api.response(404, 'Authentification failed.')
class LoginItem(Resource):
  
  @staticmethod
  def post():
    """
    Returns in header Authorization (token)
    """
    message, status, token = login(request.json)
    return message, status, { "Authorization": token }
