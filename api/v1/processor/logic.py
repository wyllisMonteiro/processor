import os

from flask import request
import cv2

from api.services.upload import Upload
from api.services.processor import Processor

def apply_gray_and_save():
  image_name = request.json["filename"]
  src_img_path = Upload.get_image_path(image_name)
  is_path_valid = os.path.exists(src_img_path)

  if not is_path_valid:
    return "no image found"

  saved_img_path =  Upload.get_image_path(image_name.split('.')[0] + "_compressor.jpg")
  Processor.apply_gray_and_save(src_img_path, saved_img_path)

def apply_brightness_and_save():
  image_name = request.json["filename"]
  src_img_path = Upload.get_image_path(image_name)
  is_path_valid = os.path.exists(src_img_path)

  if not is_path_valid:
    return "no image found"

  saved_img_path =  Upload.get_image_path(image_name.split('.')[0] + "_compressor.jpg")
  level = request.json["brightness"]
  Processor.apply_brightness_and_save(src_img_path, saved_img_path, level)
