import cv2 as cv
from api.services.processor.processor import Processor


class Gray(Processor):

    def __init__(self, src_img_path, saved_img_path):
        self.src_img_path = src_img_path
        self.saved_img_path = saved_img_path

    def apply_and_save(self):
        original_image = cv.imread(self.src_img_path)
        gray_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)

        cv.imwrite(self.saved_img_path, gray_image)
