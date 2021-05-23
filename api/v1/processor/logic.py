import os

from flask import request

from api.services.upload import Upload
from api.services.processor.gray_impl import Gray
from api.services.processor.brightness_impl import Brightness
from api.services.processor.duo_tone_impl import Duo_tone

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

        saved_img_path = Upload.get_image_path(self.image_name.split('.')[0] + "_compressor.jpg")

        return src_img_path, saved_img_path

    def apply_gray_and_save(self):
        src_img_path, saved_img_path = self.__get_paths()

        processor = Gray(src_img_path, saved_img_path)
        processor.apply_and_save()


    def apply_brightness_and_save(self):
        src_img_path, saved_img_path = self.__get_paths()
        level = request.json["brightness"]

        processor = Brightness(src_img_path, saved_img_path, level)
        processor.apply_and_save()

    def apply_duo_tone_and_save(self):
        src_img_path, saved_img_path = self.__get_paths()
        exp = request.json["exp"]
        first_tone = request.json["first_tone"]
        second_tone = request.json["second_tone"]
        light = request.json["light"]

        processor = Duo_tone(src_img_path, saved_img_path, exp, first_tone, second_tone, light)
        processor.apply_and_save()
