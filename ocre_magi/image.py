
from PIL import Image as PILImage

import cv2
import numpy

class Image:

  def __init__(self, image=None):
    self.image = image
    self.negative_image = None

  def load(self, path):
    self.image = cv2.imread(path)

  def apply_grayscale(self):
    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

  def apply_gaussian_blur(self, dx, dy):
    self.image = cv2.GaussianBlur(self.image, (dx, dy), 0)

  def apply_thresholding(self):
    ret, self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    self.negative = cv2.bitwise_not(self.image)

  def apply_boxing(self):
    self.contours, self.hierarchy = self._detect_contours()
    
    for cnt in self.contours:
      x, y, w, h = cv2.boundingRect(cnt)
      self._draw_box(x, y, w, h)

  def apply_projections(self, nsections=4):

    height, width = self.image.shape
    sz = 50
    assert height == sz
    assert width == sz
    k = nsections
    q = sz / k
    v = k * k * sz * [0]

    # apply projections

    # horizontal projections
    for y in range(0, sz):
      for x in range(0, sz):
        pxl = self.image[y][x]
        if pxl:
          v[x/q+y] = 1
          x = x % q + q
      
    # vertical projections
    for x in range(0, sz):
      for y in range(0, sz):
        pxl = self.image[y][x]
        if pxl:
          v[k*height + y/q+x] = 1
          y = y % q + q

    return v


  def _detect_contours(self):
    tmp = self.negative
    contours, hierarchy = cv2.findContours(tmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy

  def _draw_box(self, x, y, width, height):
    cv2.rectangle(self.image, (x, y), (x + width, y + height), (0, 0, 0), 1)

  def _detect_lines(self):
    min_line_length = 50
    max_line_gap = 100
    lines = cv2.HoughLinesP(self.negative, 1, numpy.pi/180, 80, None, min_line_length, max_line_gap)

    if not lines:
      return

    for x1, y1, x2, y2 in lines[0]:
      self._draw_line(x1, y1, x2, y2)

  def _draw_line(self, x1, y1, x2, y2):
    cv2.line(self.image, (x1, y1), (x2, y2), (0, 255, 0), 1)
