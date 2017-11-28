

from DurakLogic import *
from GUI import Application
from WebCamCard import CardCapture

from tkinter import *

# MVC_Template_01
# 2014 May 23  by Steven Lipton http://makeAppPie.com
# Controller initializing MVC -- simplest version possible.

#
# A A Model-View-Controller framework for TKinter.
# Model: Data Structure. Controller can send messages to it, and model can respond to message.
# View : User interface elements. Controller can send messages to it. View can call methods from Controller when an event happens.
# Controller: Ties View and Model together. turns UI responses into chages in data.


#Model: Data Structure.
#   --Controller can send messages to it, and model can respond to message.
#   --Uses delegates from vc to send messages to the Controll of internal change
#   --NEVER communicates with View
#   --Has setters and getters to communicate with Controller

#View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
    
#Controller: Ties View and Model together.
#       --Performs actions based on View events.
#       --Sends messages to Model and View and gets responses
#       --Has Delegates


class MyController():

    trump_picked = False
    last_hand = None
    last_comm = None
    last_play_func = None
    
    def __init__(self,parent):
        self.parent = parent
        self.model = PlayRecommender()
        self.view = Application(master=parent, vc=self)
        self.capture = CardCapture()
        
    # Event Handlers
    def add_hand_cards(self):
        print('Add Hand')
        if not self.trump_picked:
            self.no_trump()
        else:
            cards = self.capture.get()
            self._add_hand(cards)
            self.reset_advice()
        print('---')

    def _add_hand(self, cards):
        if cards is None: return
        print('Add to Hand: {}'.format(cards))
        self.model.add_to_hand(cards)
        print('Hand: {}'.format(self.model.hand))
        self.view.set_hand(self.model.hand)
        self.last_hand = cards

    def clear_hand(self):
        print('Clear Hand')
        if not self.trump_picked:
            self.no_trump()
        else:
            self.model.reset_hand()
            print('Hand: {}'.format(self.model.hand))
            self.view.set_hand(self.model.hand)
            self.reset_advice()
        print('---')
        self.last_hand = None

    def add_comm_cards(self):
        print('Add Comm')
        if not self.trump_picked:
            self.no_trump()
        else:
            cards = self.capture.get()
            self._add_comm(cards)
            self.reset_advice()
        print('---')

    def _add_comm(self,cards):
        if cards is None: return
        print('Add to Comm: {}'.format(cards))
        self.model.add_to_community(cards)
        print('Comm: {}'.format(self.model.comm))
        self.view.set_comm(self.model.comm)
        self.last_comm = cards
        
    def clear_comm(self):
        print('Clear Comm')
        if not self.trump_picked:
            self.no_trump()
        else:
            self.model.reset_community()
            print('Comm: {}'.format(self.model.comm))
            self.view.set_comm(self.model.comm)
            self.reset_advice()
        print('---')
        self.last_comm = None
        
    def defend(self):
        print('Defend')
        if not self.trump_picked:
            self.no_trump()
        else:
            advc = self.model.get_defend_advice()
            print('Advice: {}'.format(advc))
            self.view.set_defend_advice(advc)
        print('---')
        self.last_play_func = self.defend

    def attack(self):
        print('Attack')
        if not self.trump_picked:
            self.no_trump()
        else:
            advc = self.model.get_attack_advice()
            print('Advice: {}'.format(advc))
            self.view.set_attack_advice(advc)
        print('---')
        self.last_play_func = self.attack

    def fight(self):
        print('Fight')
        if not self.trump_picked:
            self.no_trump()
        else:
            advc = self.model.get_additional_attack_advice()
            print('Advice: {}'.format(advc))
            self.view.set_fight_advice(advc)
        print('---')
        self.last_play_func = self.fight

    def reset_advice(self):
        self.last_play_func = None
        self.view.clear_advice()
        
    def no_trump(self):
        print('ERROR: Trump Suit not Defined')
        
    def pick_hearts(self):
        self.pick_trump('H')

    def pick_spades(self):
        self.pick_trump('S')

    def pick_clubs(self):
        self.pick_trump('C')

    def pick_diamonds(self):
        self.pick_trump('D')
        
    def pick_trump(self,suit):
        self.trump_picked = True
        print('Trump Changed to {}'.format(suit))
        self.model.set_trump(suit)
        print('---')
        self.view.color_trump_buttons(trump=suit)
        self.view.clear_advice()
        self.view.color_advice_buttons()
        self._add_comm(self.last_comm)
        self._add_hand(self.last_hand)
        if self.last_play_func:
            self.last_play_func()
            
def main():
    root = Tk()
    app = MyController(root)
    root.mainloop()

    
if __name__ == '__main__':
    main() 
