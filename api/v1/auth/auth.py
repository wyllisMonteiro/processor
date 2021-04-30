import logging

from flask import request, jsonify

from flask_restx import Resource
from functools import wraps
from api.v1.auth.logic import token_required, register, login
#from rest_api_demo.api.blog.serializers import category, category_with_posts
from api.restplus import api
from api.v1.database.user import User

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='Operations related to authentification')

@ns.route('/check_token')
class CheckItem(Resource):

  @token_required
  def get(self, current_user):
    return "Valid token !!"

@ns.route('/register')
@api.response(404, 'Authentification failed.')
class RegisterItem(Resource):

  #@api.marshal_with(category_with_posts)
  def post(self):
    """
    Returns message success | error
    """
    message, status = register(request.json)
    return { "message": message }, status

@ns.route('/login')
@api.response(404, 'Authentification failed.')
class LoginItem(Resource):

  def post(self):
    """
    Returns in header Authorization (token)
    """
    message, status, token = login(request.json)
    return message, status, { "Authorization": token }
