import logging.config
import os

from flask import Flask, Blueprint

from api import settings
from api.restplus import api
from werkzeug.middleware.shared_data import SharedDataMiddleware
from api.v1.database import database
from api.v1.auth.auth import ns as auth
from api.v1.upload.upload import ns as upload
from api.v1.processor.processor import ns as processor

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
# https://github.com/postrational/rest_api_demo

def configure_app(flask_app):
  flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
  flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
  flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
  flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
  flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
  flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def initialize_app(flask_app):
  configure_app(flask_app)

  blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
  api.init_app(blueprint)
  api.add_namespace(auth)
  api.add_namespace(upload)
  api.add_namespace(processor)

  flask_app.register_blueprint(blueprint)

  database.init_app(flask_app)

def main():
  initialize_app(app)
  log.info('>>>>> Starting development server at http://localhost:5000/api/v1/ <<<<<')
  app.run(debug=settings.FLASK_DEBUG)

main()
