
from PIL import Image as PILImage

import cv2
import numpy

class Image:

  def __init__(self, path):
    self.image = cv2.imread(path)

  def apply_grayscale(self):
    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

  def apply_gaussian_blur(self, dx, dy):
    self.image = cv2.GaussianBlur(self.image, (dx, dy), 0)

  def apply_thresholding(self):
    ret, self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  def contours(self):
    tmp = cv2.bitwise_not(self.image)
    contours, hierarchy = cv2.findContours(tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

  def draw_box(self, x, y, width, height):
    cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 0), 1)

