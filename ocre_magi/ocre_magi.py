
import Tkinter as tk
import ImageTk
import tkFileDialog
import tkMessageBox

#import matplotlib.pyplot as plt
#plt.plot([1,2,3,4], [1,4,9,16], '--ro')
#plt.axis([0, 6, 0, 20])
#plt.show()

from image_preprocessor import ImagePreprocessor
from neural_network import NeuralNetwork

class OCReMagi(tk.Tk):
  
  def __init__(self):
    tk.Tk.__init__(self)
    self.wm_title('OCReMagi')
    self.minsize(width=800, height=600)
    self.option_add('*tearOff', False)
    #scrollbar = tk.Scrollbar(self)
    #scrollbar.pack(side='right', fill='y')
    #listbox.config(yscrollcommand=scrollbar.set)
    #scrollbar.config(command=listbox.yview)

    self.menu = tk.Menu()
    self.config(menu=self.menu)
    self.file_menu = tk.Menu()
    self.menu.add_cascade(menu=self.file_menu, label='File')
    self.file_menu.add_command(label="Open image", command=self._open_image)
    self.file_menu.add_command(label="Quit", command=self.quit)
    self.menu.add_command(label="Preprocess", command=self._step_process)

    self.image_preprocessor = ImagePreprocessor(self)
    self.image_views = []

  def _open_image(self):
    selected_file = tkFileDialog.askopenfilename(parent=self)
    if selected_file:
      try:
        original_image_view = tk.Label(self, image=None)
        self.image_preprocessor.open(selected_file, original_image_view)
        original_image_view.pack()
        self.image_views.append(original_image_view)

      except IOError as e:
        tkMessageBox.showerror("Invalid file path", e)

  def _step_process(self):
    if not self.image_preprocessor.is_done():
      step_image = tk.Label(self, image=None)
      self.image_preprocessor._step_process(step_image)
      step_image.pack()
      self.image_preprocessor.save()
      if self.image_views:
        self.image_views.append(step_image)
        self.image_views[len(self.image_views) - 1].grid_remove()



