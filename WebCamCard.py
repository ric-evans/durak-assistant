
import CardRecognition as cr2
from Snapshot import Snapshot
from Card import Card


class CardCapture:

  def __init__(self):
    self.cr = cr2.CardRecognition()
    self.snap = Snapshot()

  def get(self):
    # get image from webcam
    path = self.snap.capture();
    
    # send image to cr
    cards = self.cr.get_cards(path)
    
    cards = [ Card(cd[0],cd[1]) for cd in cards ]
    #print(cards)
    return cards


#
# MAIN
#
if __name__ == '__main__':
  me = CardCapture()
  cards = me.get()
  print(cards)
