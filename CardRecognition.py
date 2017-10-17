"""
  Card Recognition using OpenCV
  Code from the blog post 
  
  
"""
  
import sys
import numpy as np
import cv2
import os
import time
import pickle
import ntpath
import yaml

pkl_file = 'train.pickle'

#
def pickle_training(a):

  with open(pkl_file, 'wb+') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
  #read_cr()

#
def depickle_training():
          
  with open(pkl_file, 'rb') as handle:
    b = pickle.load(handle)
  #print('pickle len: {}'.format(len(b)))
  return b

      

class CardRecognition(object):

  training = []
  trained = False
  scale = 1.5
  window_size = ( int(200*scale), int(250*scale) )#(1000,600)
  window_delay = 2000
  diffp_threshold = 10

  
  ###########################################################
  # Utility code from 
  # http://git.io/vGi60A
  # Thanks to author of the sudoku example for the wonderful blog posts!
  ##########################################################
  
  def rectify(self,h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)
  
    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
     
    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
  
    return hnew
  
  ###########################################################
  # Image Matching
  ###########################################################
  def preprocess(self,img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 2)
    tws = 21
    sws = 21 #bigger sws, slower time (linearly)
    h = 63 #bigger h, faster time, removes more noise
    blur = cv2.fastNlMeansDenoising(blur,None,h=h,templateWindowSize=tws,searchWindowSize=sws)
    #print('done {}'.format(time.time()))
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
    return thresh

  
  def gaussblur(self,img):
    return cv2.GaussianBlur(img,(5,5),5)


  def rotate180(self,img):
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst
  
  
  def imgdiff(self,img1,img2):
    img1 = self.gaussblur(img1)
    img2 = self.gaussblur(img2)
    diff = cv2.absdiff(img1,img2)  
    diff = self.gaussblur(diff)   
    flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY)

    return diff
  
  
  def find_closest_card(self,img):
    features = self.preprocess(img)
    top_hits = sorted(self.training, key=lambda x:np.sum(self.imgdiff(x[1],features)))
    card = top_hits[0]
    match = card[0]

    diff = np.sum(self.imgdiff(card[1],features))
    summed = np.sum(features)
    diffp = (diff / summed) * 100
    
    print('diff: {:.3f}% ({}/{})'.format(diffp, diff, summed) )

    if diffp > self.diffp_threshold:
      return None
    else:
      # print card, match, and runners-up
      cv2.imshow('input card',cv2.resize(self.gaussblur(features),self.window_size))
      cv2.waitKey(self.window_delay//4)
      cv2.imshow('library match',cv2.resize(self.gaussblur(card[1]),self.window_size))
      cv2.waitKey(self.window_delay//4)
      #for i in range(0):
      #  cv2.imshow('{}'.format(i+1),cv2.resize(self.gaussblur(top_hits[i+1][1]),self.window_size))
      #  cv2.waitKey(self.window_delay//4)
      cv2.imshow('difference', cv2.resize(self.imgdiff(card[1],features),self.window_size))
      cv2.waitKey(self.window_delay*4)


      return match

  
  def bounding_box(self,iterable):
    min_x = np.min([x[0][0] for x in iterable]) 
    min_y = np.min([x[0][1] for x in iterable])
    max_x = np.max([x[0][0] for x in iterable]) 
    max_y = np.max([x[0][1] for x in iterable]) 
    bb = np.array([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])
    
    return bb


  ###############################################################################
  # Card Extraction
  # card recognition code from:
  # http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python
  ###############################################################################  
  def extract_cards(self,im, numcards=0, bestmatch=False, maxcards=10):
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY) 
    
    if self.trained and numcards > 1:
      cv2.imshow('threshold',cv2.resize(thresh,self.window_size))
      cv2.waitKey(self.window_delay)
      #cv2.destroyAllWindows()
    
    # edit for openCV 3+ 
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    maxcards = min(len(contours), maxcards)
    
    if self.trained:
      for i in contours[:maxcards] :
        print('contour area: {}'.format(cv2.contourArea(i)))

    #contours = contours[:numcards]  

    warps = []
    for card_contour in contours[:maxcards]:
      peri = cv2.arcLength(card_contour,True)
      poly = cv2.approxPolyDP(card_contour,0.02*peri,True)
      if len(poly) == 4: 
        approx = self.rectify(poly)
      else:
        approx = self.rectify(self.bounding_box(poly))

      # Show Cards Window
      #'''
      if self.trained:
        #print("showing card")
        box = np.int0(approx)
        cv2.drawContours(im,[box],0,(255,255,0),6)
        cv2.imshow('camera input',cv2.resize(im,self.window_size))
        cv2.waitKey(self.window_delay//10)
      #'''

      h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
      transform = cv2.getPerspectiveTransform(approx,h)
      warps.append(cv2.warpPerspective(im,transform,(450,450)))

    if bestmatch:
      return warps[0]
    elif numcards > 0 and len(warps) > numcards:
      return warps[:numcards]
    else:
      return warps

  
  #
  # setup training with card names and contours
  #
  def set_training(self, path, import_training=None, n=None):

    if import_training:
      self.training = import_training

    else:
      for i,filename in enumerate(os.listdir(path)):
        num, suit = filename[0], filename[1]
        #print(filename)
        im = cv2.imread(os.path.join(path,filename))
        c = self.extract_cards(im,bestmatch=True)[0]
        c = self.preprocess(c)
        self.training.append( ((num,suit), c) )
        self.training.append( ((num,suit), self.rotate180(c)) )
        
        print('{}'.format(i+1))
        if n and i > n:
          break

    self.trained = True

    
  #
  # return list of cards
  #
  def get_cards(self, filename):

    print('------')
    im = cv2.imread(filename)
      
    width = im.shape[0]
    height = im.shape[1]
    if width < height:
      im = cv2.transpose(im)
      im = cv2.flip(im,1)
    
    '''
    # Debug: uncomment to see registered images
    for i,c in enumerate(self.extract_cards(im,num_cards)):
      card = self.find_closest_card(c)
      cv2.imshow(str(card),c)
      cv2.waitKey(self.window_delay//2) 
    
    '''
    cards = [self.find_closest_card(c) for c in self.extract_cards(im)]
    cards = [c for c in cards if c is not None]

    if self.trained:
      cv2.waitKey(self.window_delay*4)
      cv2.destroyAllWindows()

    return cards


  def test_cards(self,filename):
    cards = self.get_cards(filename)

    print('~~Results~~')
    
    key = self.testkey[ ntpath.basename(filename) ] * 1 # deep copy

    total = len(key)
    
    for c in cards:
      name = '{}{}'.format(c[0],c[1])
      if name in key:
        print('correct: {}'.format(name))
        key.remove(name)
      else:
        print('incorrect: {}'.format(name))

    print('non-matched: {}'.format(key))

    acc = (1 - (len(key) / total) )
    print('~~')
    print('Accuracy: {:.3f}% ({}/{})'.format(acc*100,total-len(key),total))
    print('------')

    return cards, total, acc
    
    
  #
  # init
  #
  def __init__(self, train_dir='./train_deck/', n=None):

    if train_dir == './train_deck/' and os.path.isfile(pkl_file):
      print('Loading pickled training file...')
      import_training = depickle_training()
      self.set_training(train_dir, import_training=import_training)
    else:
      print('Training...')
      self.set_training(train_dir, n=n)
      print('Pickling training file...')
      pickle_training(self.training)

    print("Done. Using {} Training Cards".format(len(self.training)))

    with open("testcards.yaml", 'r') as stream:
      try:
        self.testkey = yaml.load(stream)
      except yaml.YAMLError as exc:
        print(exc)

    
#
# MAIN
#
if __name__ == '__main__':
  cr = CardRecognition()

  path = './test'
  for filename in os.listdir(path):
      print(filename)
      cards = cr.get_cards(os.path.join(path,filename))
      print(cards)


    
