"""
  Card Recognition using OpenCV
  Code from the blog post 
  http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python
  
  Usage: 
  
    ./card_img.py filename num_cards training_image_filename training_labels_filename num_training_cards
  
  Example:
    ./card_img.py test.JPG 4 train.png train.tsv 56
    
  Note: The recognition method is not very robust; please see SIFT / SURF for a good algorithm.  
  
"""
  
import sys
import numpy as np
import cv2
import os

class CardRecognition(object):

  training = []
  trained = False
  window_size = (200,250)#(1000,600)
  window_delay = 1000
  
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
    blur = cv2.GaussianBlur(gray,(5,5),2 )
    thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
    return thresh

  
  def gaussblur(self,img):
    return cv2.GaussianBlur(img,(5,5),2)

  
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

    # print card, match, and runners-up
    cv2.imshow('card',cv2.resize(self.gaussblur(features),self.window_size))
    cv2.waitKey(self.window_delay//4)
    cv2.imshow('match',cv2.resize(self.gaussblur(card[1]),self.window_size))
    cv2.waitKey(self.window_delay//4)
    for i in range(3):
      cv2.imshow('{}'.format(i+1),cv2.resize(self.gaussblur(top_hits[i+1][1]),self.window_size))
      cv2.waitKey(self.window_delay//4)
    cv2.imshow('diff',cv2.resize(self.imgdiff(card[1],features),self.window_size))
    cv2.waitKey(self.window_delay*4)
    
    return match

  
  def bounding_box(self,iterable):
    min_x, min_y = np.min(iterable[0], axis=0)
    max_x, max_y = np.max(iterable[0], axis=0)
    return np.array([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])


  ###############################################################################
  # Card Extraction
  ###############################################################################  
  def extract_cards(self,im, numcards=1):
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY) 
    '''
    if self.trained and numcards > 1:
      cv2.imshow('image',cv2.resize(thresh,self.window_size))
      cv2.waitKey(self.window_delay)
      cv2.destroyAllWindows()
    '''
    # edit for openCV 3+ 
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]  

    warps = []
    for card_contour in contours:
      peri = cv2.arcLength(card_contour,True)
      poly = cv2.approxPolyDP(card_contour,0.02*peri,True)
      if len(poly) == 4: 
        approx = self.rectify(poly)
      else:
        approx = self.rectify(self.bounding_box(poly))

      # Show Cards Window
      '''
      if self.trained:# and False:
        print("showing card")
        box = np.int0(approx)
        cv2.drawContours(im,[box],0,(255,255,0),6)
        cv2.imshow('a',cv2.resize(im,self.window_size))
        cv2.waitKey(self.window_delay)
      ''' 
      h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)

      transform = cv2.getPerspectiveTransform(approx,h)
      warps.append(cv2.warpPerspective(im,transform,(450,450)))
              
    return warps

  
  #
  # setup training with card names and contours
  #
  def set_training(self, path):
    
    for filename in os.listdir(path):
      num, suit = filename[0], filename[1]
      #print(filename)
      im = cv2.imread(os.path.join(path,filename))
      c = self.extract_cards(im)[0]
      self.training.append( ((num,suit), self.preprocess(c)) )

    self.trained = True
    '''
    labels = {}
    for line in open(training_labels_filename): 
      key, num, suit = line.strip().split()
      labels[int(key)] = (num,suit)
      
    #print("Training")
  
    im = cv2.imread(training_image_filename)
    for i,c in enumerate(self.extract_cards(im,num_training_cards)):
      if avoid_cards is None or (labels[i][0] not in avoid_cards[0] and labels[i][1] not in avoid_cards[1]):
        self.training[i] = (labels[i], self.preprocess(c))
    
    #print("Done training")
    '''

  #
  # return list of cards
  #
  def get_cards(self,filename,num_cards):
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
    cards = [self.find_closest_card(c) for c in self.extract_cards(im,num_cards)]
    return cards

  
  #
  # init
  #
  def __init__(self, train_dir='./train_deck/'):
    self.set_training(train_dir)
    print("Finished Training {} Cards".format(len(self.training)))
      
#
# MAIN
#
if __name__ == '__main__':
  cr = CardRecognition()

  path = './test'
  for filename in os.listdir(path):
      print(filename)
      cards = cr.get_cards(os.path.join(path,filename), 4)
      print(cards)


    
