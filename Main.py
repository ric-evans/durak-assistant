

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
    
    def __init__(self,parent):
        self.parent = parent
        self.model = PlayRecommender()
        self.view = Application(master=parent, vc=self)
        self.capture = CardCapture()
        
    # Event Handlers
    def add_hand_cards(self):
        print('Add Hand')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            cards = self.capture.get()
            print('Add to Hand: {}'.format(cards))
            self.model.add_to_hand(cards)
            print('Hand: {}'.format(self.model.hand))
            self.view.set_hand(self.model.hand)
            self.view.clear_advice()
        print('---')

    def clear_hand(self):
        print('Clear Hand')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            self.model.reset_hand()
            print('Hand: {}'.format(self.model.hand))
            self.view.set_hand(self.model.hand)
            self.view.clear_advice()
        print('---')

    def add_comm_cards(self):
        print('Add Comm')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            cards = self.capture.get()
            print('Add to Comm: {}'.format(cards))
            self.model.add_to_community(cards)
            print('Comm: {}'.format(self.model.comm))
            self.view.set_comm(self.model.comm)
            self.view.clear_advice()
        print('---')
        
    def clear_comm(self):
        print('Clear Comm')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            self.model.reset_community()
            print('Comm: {}'.format(self.model.comm))
            self.view.set_comm(self.model.comm)
            self.view.clear_advice()
        print('---')
        
    def defend(self):
        print('Defend')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            advc = self.model.get_defend_advice()
            print('Advice: {}'.format(advc))
            self.view.set_defend_advice(advc)
        print('---')

    def attack(self):
        print('Attack')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            advc = self.model.get_attack_advice()
            print('Advice: {}'.format(advc))
            self.view.set_attack_advice(advc)
        print('---')

    def fight(self):
        print('Fight')
        if not self.trump_picked:
            print('ERROR: Trump Suit not Defined')
        else:
            advc = self.model.get_additional_attack_advice()
            print('Advice: {}'.format(advc))
            self.view.set_fight_advice(advc)
        print('---')

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


        
def main():
    root = Tk()
    app = MyController(root)
    root.mainloop()

    
if __name__ == '__main__':
    main() 
