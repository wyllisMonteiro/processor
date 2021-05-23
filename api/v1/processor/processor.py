import logging
import os

from flask import request

from flask_restx import Resource
from api.restplus import api
from api.v1.auth.logic import token_required
from api.v1.processor.logic import Logic

log = logging.getLogger(__name__)

ns = api.namespace('images', description='Operations related to image processor')

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

logic = Logic()

@ns.route('/gray')
class ImageGrayItem(Resource):

    @staticmethod
    @token_required
    def post(current_user):
        """
        Returns gray image
        """
        logic.set_image_name(request.json["filename"])

        try:
            logic.apply_gray_and_save()
            return "success"
        except ValueError as error:
            return error.args


@ns.route('/brightness')
class ImageBrightnessItem(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        """
        Returns brightness image
        """
        logic.set_image_name(request.json["filename"])

        try:
            logic.apply_brightness_and_save()
            return "success"
        except ValueError as error:
            return error.args


@ns.route('/duo_tone')
class ImageDuoToneItem(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        """
        Returns brightness image
        """
        logic.set_image_name(request.json["filename"])

        try:
            logic.apply_duo_tone_and_save()
            return "success"
        except ValueError as error:
            return error.args
