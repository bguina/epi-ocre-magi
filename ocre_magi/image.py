
from PIL import Image as PILImage

import cv2

class Image:

  def __init__(self, path=None):
    self.image = None
    if path:
      self.open(path)

  def open(self, path):
    self.image = cv2.imread(path)

  def apply_bw(self):
    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

  def apply_gaussian_blur(self, dx, dy):
    self.image = cv2.GaussianBlur(self.image, (dx, dy), 0)

  def apply_otsu_binarization(self):
    ret, self.image = cv2.threshold(self.image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  def apply_bounding_box(self):
    tmp = cv2.bitwise_not(self.image)
    contours, hierarchy = cv2.findContours(tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    for cnt in contours:
      i += 1
      x, y, w, h = cv2.boundingRect(cnt)
      cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 0, 0), 1)
