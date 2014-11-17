
import Tkinter as tk
import ImageTk
import tkFileDialog
import tkMessageBox

import PIL

from processor import Processor
from neural_network import NeuralNetwork

class OCReMagi(tk.Tk):
  
  def __init__(self, image_path=None, process_image=False):
    tk.Tk.__init__(self)
    self.wm_title('OCReMagi')
    self.minsize(width=800, height=600)
    self.option_add('*tearOff', False)

    self.menu = tk.Menu()
    self.config(menu=self.menu)
    self.menu.add_command(label="Open image", command=self._on_open_image)
    self.menu.add_command(label="Step process", command=self._on_step_process)
    self.menu.add_command(label="Quit", command=self.quit)

    self.view = tk.Label(self, image=None)
    self.view.pack(fill='both')

    self.processor = Processor(self)

    if image_path:
      self._load(image_path)
      
      if process_image:
        while not self.processor.is_done():
          self.processor.step_process()

        self._render()

  def _load(self, image_path):
    if image_path:
      try:
        self.processor.open(image_path)

      except IOError as e:
        tkMessageBox.showerror("Invalid file path", e)
    
      self._render()

  def _on_open_image(self):
    self._load(tkFileDialog.askopenfilename(parent=self))

  def _on_step_process(self):
    if not self.processor.is_done():
      self.processor.step_process()
      self._render()

  def _render(self):
    self.view.tkimage = ImageTk.PhotoImage(PIL.Image.fromarray(self.processor.image.image))
    self.view.configure(image=self.view.tkimage)

    
