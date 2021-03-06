#!/usr/bin/env python

import os
import sys
import string
import logging
import re

import numpy
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer

# save/load networks (thus their weights)
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.utilities           import percentError

from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
from pybrain.structure.modules   import SoftmaxLayer

import operator

from image import Image
import cv2

class NeuralNetwork:
  DEFAULT_PATH = 'default.txt'
  # Targets are the characters in the following string:
  #<string>0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ </string>
  TARGETS = string.printable[:-5] # trailing "\t\n\r\x0b\x0c" characters must be ignored. the space character remains.
  LABELS = ['num_' + TARGETS[i]                       for i in xrange(0, 10)] + [        # numbers
    TARGETS[i].lower() + ('_small' if i < 36 else '') for i in xrange(10, 62)] + [       # lower (10,36) and upper (36,62) alpha 
    'sym_' + ['exclmark','quotmark','num','dollar','pcent','amper','apos','lparen','rparen','star','plus','comma','hyphen',
    'point','slash','colon','scolon','lthan', 'equal','gthan','questmark','arob', 'lsqbracket',
    'bslash','rsqbracket','caret','under','bquote','lcbracket','pipe','rcbracket','tilde','space',][i-62] 
                                                      for i in xrange(62, len(TARGETS))] # symbols (ascii order from range 62)
  
  def __init__(self, name, log_level=logging.WARNING):
    self.logger = logging.getLogger('neural_network')
    self.logger.setLevel(log_level)
    self.name = name
    self.base_path = os.path.relpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    self.save_path = os.path.join(self.base_path, 'networks', self.name + '.xml')
    self.train_path = os.path.join(self.base_path, 'training')
    self.test_path = os.path.join(self.base_path, 'test')
    self.logger.info('using network {0}'.format(self.name))
    #self.net = buildNetwork(1, 5, len(self.TARGETS), outclass=SoftmaxLayer)
    self.net = buildNetwork(10*50, 5, len(self.TARGETS), outclass=SoftmaxLayer)
    if os.path.exists(self.save_path):
      self.load()
  
  def load(self):
    loaded = False
    if os.path.exists(self.save_path):
      try:
        self.net = NetworkReader.readFrom(self.save_path)
        loaded = True
      except Exception as e:
        e = str(e)
    else:
      e = '{1} does not exist'.format(self.name, self.save_path)

    if loaded:
      self.logger.info('loaded {0}'.format(self.name, self.save_path))
    else:
      self.logger.error('error loading {0} from {1}: {2}'.format(self.name, self.save_path, e))
      sys.exit(2)

  def recognize(self, projections):
    probs = self.net.activate(projections)
    results = {self.LABELS[i]: probs[i] for i in range(len(probs))}
    top_res = sorted(results.items(), key = operator.itemgetter(1), reverse = True)[:5]
    return top_res

  def train(self):

    def fetch_datasets(self, path):
      ds = ClassificationDataSet(10*50, target=1, nb_classes=len(self.TARGETS), class_labels=self.LABELS)
     
      for dir_path in os.listdir(path):
        if dir_path[0] == '.':
          continue
          
        for file_path in os.listdir(os.path.join(path, dir_path)):
          if file_path[-3:] == '.db':
            continue

          matched = False
          for i in range(len(self.LABELS)):
            label_match = re.match('^(.*(_|-))?{0}\.(bmp|png)$'.format(self.LABELS[i]), file_path)
            if label_match:
              self.logger.info('adding sample {0}, target: {1}'.format(file_path, self.LABELS[i]))
              image = Image()
              image.load(os.path.join(path, dir_path, file_path))

              image.apply_grayscale()
              image.apply_gaussian_blur(3, 3)
              image.apply_thresholding()
              v = image.apply_projections()
              
              #for y in range(50):
              #  for x in range(50):
              #    print image.image[y][x],
              #  print            
              
              #cv2.imshow('dst_rt', image.image)
              #cv2.waitKey(0)
              #cv2.destroyAllWindows()
              

              ds.addSample(v, i)
              
              matched = True

          if not matched:
            self.logger.error('file {0} does not match any target label'.format(file_path))
            sys.exit(2)

      return ds

    trndata = fetch_datasets(self, self.train_path)
    tstdata = fetch_datasets(self, self.test_path)
    tstdata._convertToOneOfMany()
    trndata._convertToOneOfMany()
    #trainer = BackpropTrainer(self.net, dataset=trndata, momentum=0.99, verbose=True, weightdecay=0.01)
    trainer = BackpropTrainer(self.net, trndata)
    
    try:
      #self.logger.info('training\n{0}'.format(str(trainer.trainUntilConvergence())))
      #self.logger.info('training\n')
      while True:
        trainer.trainEpochs(50)

        trnresult = percentError( trainer.testOnClassData(), trndata['class'])
        tstresult = percentError( trainer.testOnClassData( dataset=tstdata ), tstdata['class'] )

        print "epoch: %4d" % trainer.totalepochs, "  train error: %5.2f%%" % trnresult, "  test error: %5.2f%%" % tstresult

    except KeyboardInterrupt as e:
      self.logger.info('\ntraining interrupted, saving before exiting...'.format(self.name, self.save_path))
      self.save()

  def save(self):
    saved = False
    try:
      NetworkWriter.writeToFile(self.net, self.save_path)
      saved = True
    except Exception as e:
      e = str(e)
    
    if saved:
      self.logger.info('saved {0} as {1}'.format(self.name, self.save_path))
    else:
      self.logger.error('error saving {0} as {1}: {2}'.format(self.name, self.save_path, e))
      sys.exit(2)
      

def main(network_name, action, verbose=False):

  def delete(network, critical=True):
    try:
      os.remove(network.save_path)
      network.logger.error('deleted {0}'.format(network.name))
    except OSError as e:
      if critical:
        network.logger.error('error deleting {0}: {1}'.format(network.name, str(e)))
        sys.exit(2)

  def create(network):
    network.save()
  
  def train(network):
    network.train()

  actions = {
    'delete': delete,
    'create': create,
    'train': train,
  }
 
  log_level = logging.DEBUG if verbose else logging.WARNING
  network = NeuralNetwork(network_name, log_level=log_level)
  actions[action](network)

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='OCR program')
  parser.add_argument('network', help='network name')
  parser.add_argument('action', choices=('delete', 'create', 'train', ), help='operation to perform')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='print debug info')
  args = parser.parse_args()
  main(args.network, args.action, args.verbose)

