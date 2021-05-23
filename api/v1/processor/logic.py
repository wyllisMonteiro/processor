import os

from flask import request

from api.services.upload import Upload
from api.services.processor.gray_impl import Gray
from api.services.processor.brightness_impl import Brightness
from api.services.processor.duo_tone_impl import DuoTone, DuoToneInfo


class Logic:
    def __init__(self, image_name=""):
        self.image_name = image_name

    def set_image_name(self, value):
        self.image_name = value

    def __get_paths(self):
        src_img_path = Upload.get_image_path(self.image_name)
        is_path_valid = os.path.exists(src_img_path)

        if not is_path_valid:
            raise ValueError("Image not found")

        saved_image_name = self.image_name.split('.')[0] + "_compressor.jpg"
        saved_img_path = Upload.get_image_path(saved_image_name)

        return src_img_path, saved_img_path, saved_image_name

    def apply_gray_and_save(self):
        src_img_path, saved_img_path, saved_image_name = self.__get_paths()

        processor = Gray(src_img_path, saved_img_path)
        processor.apply_and_save()

        return saved_image_name

    def apply_brightness_and_save(self):
        src_img_path, saved_img_path, saved_image_name = self.__get_paths()
        level = request.json["brightness"]

        processor = Brightness(src_img_path, saved_img_path, level)
        processor.apply_and_save()

        return saved_image_name

    def apply_duo_tone_and_save(self):
        src_img_path, saved_img_path, saved_image_name = self.__get_paths()
        exp = request.json["exp"]
        first_tone = request.json["first_tone"]
        second_tone = request.json["second_tone"]
        light = request.json["light"]

        duo_tone_info = DuoToneInfo(exp, first_tone, second_tone, light)
        processor = DuoTone(src_img_path, saved_img_path, duo_tone_info)
        processor.apply_and_save()

        return saved_image_name
