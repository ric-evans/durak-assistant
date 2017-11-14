

from DurakLogic import *
from GUI import Application
from WebCamCard import CardCapture

from tkinter import *

#MVC_Template_01
#2014 May 23  by Steven Lipton http://makeAppPie.com
#Controller initializing MVC -- simplest version possible.

#
# A A Model-View-Controller framework for TKinter.
# Model: Data Structure. Controller can send messages to it, and model can respond to message.
# View : User interface elements. Controller can send messages to it. View can call methods from Controller when an event happens.
# Controller: Ties View and Model together. turns UI responses into chages in data.

#
#Controller: Ties View and Model together.
#       --Performs actions based on View events.
#       --Sends messages to Model and View and gets responses
#       --Has Delegates

class MyController():
    def __init__(self,parent):
        self.parent = parent
        trump = 'H'
        self.model = PlayRecommender(trump)
        print('Trump Suit: {}'.format(trump))
        self.view = Application(master=parent, vc=self)
        self.capture = CardCapture()
        
        
    # Event Handlers
    def add_hand_cards(self):
        cards = self.capture.get()
        print('Add to Hand: {}'.format(cards))
        self.model.add_to_hand(cards)
        print('Hand: {}'.format(self.model.hand))
        print('---')
        self.view.update_hand(self.model.hand)

    def clear_hand(self):
        print('Clear Hand')
        self.model.reset_hand()
        print('Hand: {}'.format(self.model.hand))
        print('---')
        self.view.update_hand(self.model.hand)

    def add_comm_cards(self):
        cards = self.capture.get()
        print('Add to Comm: {}'.format(cards))
        self.model.add_to_community(cards)
        print('Comm: {}'.format(self.model.comm))
        print('---')
        self.view.update_comm(self.model.comm)
        
    def clear_comm(self):
        print('Clear Comm')
        self.model.reset_community()
        print('Comm: {}'.format(self.model.comm))
        print('---')
        self.view.update_comm(self.model.comm)
        
    def defend(self):
        print('Defend')
        advc = self.model.defend_advice()
        print('Advice: {}'.format(advc))
        print('---')
        self.view.update_advice(advc)

    def attack(self):
        print('Attack')
        advc = self.model.attack_advice()
        print('Advice: {}'.format(advc))
        print('---')
        self.view.update_advice(advc)

    def fight(self):
        print('Fight')
        advc = self.model.additional_attack_advice()
        print('Advice: {}'.format(advc))
        print('---')
        self.view.update_advice(advc)
                
        
#View : User interface elements.
#       --Controller can send messages to it.
#       --View can call methods from Controller vc when an event happens.
#       --NEVER communicates with Model.
#       --Has setters and getters to communicate with controller
    
        
#Model: Data Structure.
#   --Controller can send messages to it, and model can respond to message.
#   --Uses delegates from vc to send messages to the Controll of internal change
#   --NEVER communicates with View
#   --Has setters and getters to communicate with Controller


def main():
    root = Tk()
    app = MyController(root)
    root.mainloop()

    
if __name__ == '__main__':
    main() 
