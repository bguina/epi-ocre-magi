
from PIL import Image

class Image:
  
  def __init__(self, path):
    self.load(path)

  def load(self, path):
    self.image = Image.open(path)

  def preprocess(self):
    gray = self.image.convert('L')
    self.image = gray.point(lambda x: 255 if x<128 else 0, '1')
    #self.image..save("output/result_bw.png")

  def save(self, path):
    self.image.save(path)


