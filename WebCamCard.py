
import CardRecognition as cr2
from Snapshot import Snapshot
import os


#
# MAIN
#
if __name__ == '__main__':

  cr = cr2.CardRecognition()
  snap = Snapshot()
  
  # get image from webcam
  path = snap.capture();

  # send image to cr
  cards = cr.get_cards(path)

  print(cards)

