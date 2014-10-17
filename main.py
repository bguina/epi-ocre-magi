#!/usr/bin/env python

from PIL import Image

def main():
  col = Image.open("assets/captcha-samples.png")
  gray = col.convert('L')
  bw = gray.point(lambda x: 255 if x<128 else 0, '1')
  bw.save("output/result_bw.png")

if __name__ == '__main__':
  main()

