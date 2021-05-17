import logging
import traceback2 as traceback

from flask_restx import Api
from sqlalchemy.orm.exc import NoResultFound
from api import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='Processor API',
          description='Image processing API')


@api.errorhandler
def default_error_handler():
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

    return {'message': "No error"}, 200


@api.errorhandler(NoResultFound)
def database_not_found_error_handler():
    """No results found in database"""
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
