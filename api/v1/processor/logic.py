import os

from flask import request

from api.services.upload import Upload
from api.services.processor.gray_impl import Gray
from api.services.processor.brightness_impl import Brightness


def apply_gray_and_save():
    image_name = request.json["filename"]
    src_img_path = Upload.get_image_path(image_name)
    is_path_valid = os.path.exists(src_img_path)

    if not is_path_valid:
        return "no image found"

    saved_img_path = Upload.get_image_path(image_name.split('.')[0] + "_compressor.jpg")

    processor = Gray(src_img_path, saved_img_path)
    processor.apply_and_save()


def apply_brightness_and_save():
    image_name = request.json["filename"]
    src_img_path = Upload.get_image_path(image_name)
    is_path_valid = os.path.exists(src_img_path)

    if not is_path_valid:
        return "no image found"

    saved_img_path = Upload.get_image_path(image_name.split('.')[0] + "_compressor.jpg")
    level = request.json["brightness"]

    processor = Brightness(src_img_path, saved_img_path, level)
    processor.apply_and_save()
