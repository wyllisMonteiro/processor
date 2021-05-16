import os

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

class Upload:

  @staticmethod
  def get_image_path(image_name):
    basedir = os.path.join(os.path.realpath(os.path.dirname(__file__)), '../..')
    uploads_dir = os.path.join(basedir, UPLOAD_FOLDER)
    return os.path.join(uploads_dir, image_name)
