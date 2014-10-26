
import Tkinter as tk

#import matplotlib.pyplot as plt
#plt.plot([1,2,3,4], [1,4,9,16], '--ro')
#plt.axis([0, 6, 0, 20])
#plt.show()

from neural_network import NeuralNetwork
from image import Image

class OCReMagi(tk.Frame):
  
  def __init__(self):
    tk.Frame.__init__(self, None)
    self.master.title('OCReMagi')
    self.grid()
    self._create_widgets()

  # private
  def _create_widgets(self):
    self.quitButton = tk.Button(self, text='Quit', command=self.quit)
    self.quitButton.grid()

  def _recognize_character(self):
    pass

  def _recognize_text(self):
    pass

