from api.services.processor.processor import Processor
import cv2 as cv

class Brightness(Processor):

    def __init__(self, src_img_path, saved_img_path, level):
        self.src_img_path = src_img_path
        self.saved_img_path = saved_img_path
        self.level = level

    def apply_and_save(self):
        original_image = cv.imread(self.src_img_path)
        brightness_image = cv.convertScaleAbs(original_image, beta=self.level)

        cv.imwrite(self.saved_img_path, brightness_image)
