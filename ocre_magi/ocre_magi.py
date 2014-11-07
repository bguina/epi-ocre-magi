
import Tkinter as tk
import ImageTk
import tkFileDialog
import tkMessageBox

import PIL

from processor import Processor
from neural_network import NeuralNetwork

class OCReMagi(tk.Tk):
  
  def __init__(self):
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

  def _on_open_image(self):
    selected_file = tkFileDialog.askopenfilename(parent=self)
    if selected_file:
      try:
        self.processor.open(selected_file)

      except IOError as e:
        tkMessageBox.showerror("Invalid file path", e)

    self._render()

  def _on_step_process(self):
    if not self.processor.is_done():
      self.processor.step_process()
      self._render()

  def _render(self):
      self.view.tkimage = ImageTk.PhotoImage(PIL.Image.fromarray(self.processor.image.image))
      self.view.configure(image=self.view.tkimage)

    
