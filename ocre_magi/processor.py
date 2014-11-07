import Tkinter as tk
from PIL import Image as PILImage

from image import Image

class Processor:

  def __init__(self, parent):
    self.steps = (
      self._step_bw,
      self._step_blur,
      self._step_otsu,
      self._step_rotate,
    )
    self.image = None

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
    print 'step process {0}'.format(step_function.__name__)
    step_function()
    self.current_step += 1

  def _step_bw(self):
    self.image.apply_bw()

  def _step_blur(self):
    self.image.apply_gaussian_blur(3, 3)

  def _step_otsu(self):
    self.image.apply_otsu_binarization()

  def _step_rotate(self):
    pass



