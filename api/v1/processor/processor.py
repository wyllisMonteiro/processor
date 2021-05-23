import logging
import os

from flask import request, redirect, url_for

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
    def post(
        current_user  # pylint: disable=unused-argument
    ):
        """
        Returns gray image
        """
        logic.set_image_name(request.json["filename"])

        try:
            saved_filename = logic.apply_gray_and_save()
            return redirect(url_for('api._uploaded_image_item', filename=saved_filename))
        except ValueError as error:
            return error.args


@ns.route('/brightness')
class ImageBrightnessItem(Resource):
    @staticmethod
    @token_required
    def post(
        current_user  # pylint: disable=unused-argument
    ):
        """
        Returns brightness image
        """
        logic.set_image_name(request.json["filename"])

        try:
            saved_filename = logic.apply_brightness_and_save()
            return redirect(url_for('api._uploaded_image_item', filename=saved_filename))
        except ValueError as error:
            return error.args


@ns.route('/duo_tone')
class ImageDuoToneItem(Resource):
    @staticmethod
    @token_required
    def post(
        current_user  # pylint: disable=unused-argument
    ):
        """
        Returns brightness image
        """
        logic.set_image_name(request.json["filename"])

        try:
            saved_filename = logic.apply_duo_tone_and_save()
            return redirect(url_for('api._uploaded_image_item', filename=saved_filename))
        except ValueError as error:
            return error.args
