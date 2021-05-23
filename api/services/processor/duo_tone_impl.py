import cv2 as cv
import numpy as np
from api.services.processor.processor import Processor

MIN_EXP = 0
MAX_EXP = 10
DARK_IMAGE = 0
LIGHT_IMAGE = 1


class DuoTone(Processor):
    def __init__(
            self,
            src_img_path,
            saved_img_path,
            duo_tone_info
    ):
        self.src_img_path = src_img_path
        self.saved_img_path = saved_img_path
        self.duo_tone_info = duo_tone_info

    def apply_and_save(self):
        original_image = cv.imread(self.src_img_path)
        brightness_image = self.__apply_duo_tone(original_image)

        cv.imwrite(self.saved_img_path, brightness_image)

    def __apply_duo_tone(self, img):
        """
        4 values to create duo tone
        - exponent for hue [0 - 10]
        - BGR [0 - 2]
        - BGR [0 - 3]
        - Light [0 - 1]
        :param img: using cv.imread()
        :return: img
        """
        exp = self.duo_tone_info.exp
        first_color = self.duo_tone_info.first_color
        second_color = self.duo_tone_info.second_color
        light = self.duo_tone_info.light
        while True:
            exp = 1 + exp/ 100  # convert to range: [1 - 2]
            duo_tone_img = img.copy()
            for i in range(3):
                if i in (first_color, second_color):  # if channel is present
                    duo_tone_img[:, :, i] = DuoTone.exponential_function(
                        duo_tone_img[:, :, i],
                        exp
                    )  # increasing the values if channel selected
                else:
                    if light:
                        duo_tone_img[:, :, i] = self.exponential_function(
                            duo_tone_img[:, :, i],
                            2 - exp
                        )  # reducing value to make the channels light
                    else:
                        duo_tone_img[:, :, i] = 0  # converting the whole channel to 0
            return duo_tone_img

    @staticmethod
    def exponential_function(channel, exp):
        table = np.array([min((i ** exp), 255) for i in np.arange(0, 256)]).astype(
            "uint8")  # generating table for exponential function
        channel = cv.LUT(channel, table)
        return channel


class DuoToneInfo:
    first_tone_available = {
        "blue": 0,
        "green": 1,
        "red": 2
    }

    second_tone_available = {
        "blue": 0,
        "green": 1,
        "red": 2,
        "none": 3
    }

    def __init__(
            self,
            exp,
            first_color,
            second_color,
            light
    ):
        if MIN_EXP >= exp > MAX_EXP:
            print("false")

        if first_color not in self.first_tone_available.values():
            print("false")

        if second_color not in self.second_tone_available.values():
            print("false")

        if LIGHT_IMAGE >= light >= DARK_IMAGE:
            print("false")

        self.exp = exp
        self.first_color = self.first_tone_available[first_color]
        self.second_color = self.second_tone_available[second_color]
        self.light = light
