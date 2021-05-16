import logging
import os

from flask_restx import Resource
from api.restplus import api
from api.v1.auth.logic import token_required
from api.v1.processor.logic import apply_gray_and_save, apply_brightness_and_save

log = logging.getLogger(__name__)

ns = api.namespace('images', description='Operations related to image processor')

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

@ns.route('/gray')
class ImageGrayItem(Resource):

  @staticmethod
  @token_required
  def post(current_user):
    """
    Returns gray image
    """
    apply_gray_and_save()

    return "success"

@ns.route('/brightness')
class ImageBrightnessItem(Resource):
  @staticmethod
  @token_required
  def post(current_user):
    """
    Returns brightness image
    """
    apply_brightness_and_save()

    return "success"
