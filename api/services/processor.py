import cv2

class Processor:

  @staticmethod
  def apply_gray_and_save(src_img_path, saved_img_path):
    original_image = cv2.imread(src_img_path)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(saved_img_path, gray_image)

  @staticmethod
  def apply_brightness_and_save(src_img_path, saved_img_path, level):
    original_image = cv2.imread(src_img_path)
    gray_image = cv2.convertScaleAbs(original_image, beta=level)
    
    cv2.imwrite(saved_img_path, gray_image)
