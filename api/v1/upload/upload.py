import logging
import os

from flask import request, redirect, url_for, send_from_directory

from flask_restx import Resource
from werkzeug.utils import secure_filename
from api.v1.auth.logic import token_required
from api.v1.upload.logic import allowed_file
from api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('', description='Operations related to upload of images')

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

@ns.route('/uploaded_image')
class UploadedImageItem(Resource):

  def post(self):
    basedir = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../../..')
    uploads_dir = os.path.join(basedir, UPLOAD_FOLDER)
    file_name = request.args.get("filename")
    return send_from_directory(uploads_dir, file_name)

@ns.route('/uploads/images')
class UploadImageItem(Resource):

  @token_required
  def post(self):
    if 'file' not in request.files:
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(UPLOAD_FOLDER, filename))
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
