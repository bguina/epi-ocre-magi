#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ocre_magi

def main(image_path=None, process_image=False):
  ocre_magi.OCReMagi(image_path, process_image).mainloop()

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='OCR program')
  parser.add_argument('-f', dest='image', default=None, help='image path to load')
  parser.add_argument('--process', dest='process_image', action='store_true', help='process all the steps on the loaded image using -f')
  args = parser.parse_args()
  main(args.image, args.process_image)

