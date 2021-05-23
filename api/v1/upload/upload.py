import logging
import os

from flask import request, redirect, url_for, send_from_directory

from flask_restx import Resource
from werkzeug.utils import secure_filename
from api.v1.auth.logic import token_required
from api.v1.upload.logic import allowed_file
from api.restplus import api
from api.services.upload import Upload

log = logging.getLogger(__name__)

ns = api.namespace('', description='Operations related to upload of images')


@ns.route('/uploaded_image')
class UploadedImageItem(Resource):

    @staticmethod
    def post():
        """
        Returns image uploaded
        """
        uploads_path = Upload.get_image_path("")
        file_name = request.args.get("filename")
        return send_from_directory(uploads_path, file_name)

    @staticmethod
    def get():
        """
        Returns image uploaded
        """
        uploads_path = Upload.get_image_path("")
        file_name = request.args.get("filename")
        return send_from_directory(uploads_path, file_name)


@ns.route('/uploads/images')
class UploadImageItem(Resource):

    @staticmethod
    @token_required
    def post(
        current_user  # pylint: disable=unused-argument
    ):
        """
        Returns image uploaded
        """
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = os.getenv("UPLOAD_FOLDER")
            file.save(os.path.join(upload_folder, filename))
            return redirect(url_for('api._uploaded_image_item', filename=filename))
        return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
              <input type=file name=file>
              <input type=submit value=Upload>
            </form>
        '''
