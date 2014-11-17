import Tkinter as tk
from PIL import Image as PILImage
import cv2

from image import Image

class Processor:

  def __init__(self, parent):
    self.steps = (
      self._step_grayscale,
      self._step_blur,
      self._step_tresholding,
      self._step_boxing,
      self._step_crossing,
    )
    self.image = None
    self.inputs = []


  def open(self, path):
    self.current_step = 0
    self.image = Image(path)
    return self.image

  def is_done(self):
    if self.image is not None and self.current_step < len(self.steps):
      return False
    return True

  def step_process(self):
    step_function = self.steps[self.current_step]
    print 'step process: {0}'.format(step_function.__name__[len('_step_'):])
    step_function()
    self.current_step += 1

  def _step_grayscale(self):
    self.image.apply_grayscale()

  def _step_blur(self):
    self.image.apply_gaussian_blur(3, 3)

  def _step_tresholding(self):
    self.image.apply_thresholding()

  def _step_boxing(self):
    self.contours, self.hierarchy = self.image.contours()
    
    for cnt in self.contours:
      x, y, w, h = cv2.boundingRect(cnt)
      self.image.draw_box(x, y, w, h)

  def _step_crossing(self):
    pass

