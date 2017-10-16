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
    
  def imgdiff(self,img1,img2):
    img1 = cv2.GaussianBlur(img1,(5,5),5)
    img2 = cv2.GaussianBlur(img2,(5,5),5)    
    diff = cv2.absdiff(img1,img2)  
    diff = cv2.GaussianBlur(diff,(5,5),5)    
    flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY) 
    return np.sum(diff)  
  
  def find_closest_card(self,img):
    features = self.preprocess(img)
    return sorted(self.training, key=lambda x:self.imgdiff(x[1],features))[0][0]
    
     
  ###############################################################################
  # Card Extraction
  ###############################################################################  
  def extract_cards(self,im, numcards=4):
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY) 
  
    # edit for openCV 3+ 
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]  

    warps = []
    for card in contours:
      try:
        peri = cv2.arcLength(card,True)
        approx = self.rectify(cv2.approxPolyDP(card,0.02*peri,True))
      
        # Show Cards Window
        if self.training is not None and len(self.training) == 2*52:
          print("showing card")
          box = np.int0(approx)
          cv2.drawContours(im,[box],0,(255,255,0),6)
          imx = cv2.resize(im,(1000,600))
          cv2.imshow('a',imx)
          cv2.waitKey(1500)
          
        h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
        
        transform = cv2.getPerspectiveTransform(approx,h)
        warps.append(cv2.warpPerspective(im,transform,(450,450)))
      except:
        print('No match')
        
    return warps

  
  #
  # setup training with card names and contours
  #
  def set_training(self, path):
    
    for filename in os.listdir(path):
      num, suit = filename[0], filename[1]
      #print(filename)
      im = cv2.imread(os.path.join(path,filename))
      c = self.extract_cards(im,1)[0]
      self.training.append( ((num,suit), self.preprocess(c)) )

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
  
    # Debug: uncomment to see registered images
    for i,c in enumerate(self.extract_cards(im,num_cards)):
      card = self.find_closest_card(c)
      cv2.imshow(str(card),c)
      cv2.waitKey(1000) 
      
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


    
