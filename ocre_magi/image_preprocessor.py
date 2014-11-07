
from PIL import Image as PILImage

import Tkinter as tk
import ImageTk


class ImagePreprocessor:

  def __init__(self, parent, image_type='character'):
    if image_type not in ('character', 'text', ):
      raise Exception

    self.image_type = image_type
    self.step = 0
    self.steps = {
      'character': {
        0: self._preprocess_bw,
        1: self._preprocess_character,
        2: self._preprocess_binarize,
      },
      'text': {
        0: self._preprocess_bw,
        1: self._preprocess_text,
        2: self._preprocess_binarize,
      },
    }
    self.image = None
    self.view = tk.Label(parent, image=None)
    self.view.pack(fill='both')

  def open(self, path, image_view=None):
    self.image = PILImage.open(path)
    if image_view:
      self._render(image_view)

  def process(self):
    while not self.is_done:
      self._step_process(image_type)
  
  def is_done(self):
    if self.image is not None and self.step in self.steps[self.image_type]:
      return False
    return True

  def _step_process(self, image_view=None):
    step_callback = self.steps[self.image_type][self.step]
    print 'step_process {0}'.format(step_callback.__name__)
    step_callback()
    self.step += 1
    if image_view:
      self._render(image_view)

  def _preprocess_bw(self):
    # to grayscale to black and white threshold
    self.image = self.image.convert('L').point(lambda x: 255 if x > 128 else 0, '1')
    self.image.getpixel((5,5))

  def _preprocess_character(self):
    # see 
    # document rotation by if not called from a _preprocess_text
    pass

  def _preprocess_text(self):
    # document rotation by baselines detection
    pass

  def _preprocess_binarize(self):
    # line crossing
    pass

  # takes a tk.Label and renders its image in it
  def _render(self, image_view):
    image_view.tkimage = ImageTk.PhotoImage(self.image)
    image_view.configure(image=image_view.tkimage)
    image_view.pack()

  def save(self):
    self.image.save("output/result_bw.png")
    
