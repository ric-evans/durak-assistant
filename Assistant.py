


import CardRecognition as cr2
import pickle
import os
                    
class Assistant(object):

    #
    # init
    #
    def __init__(self):
        pass
        
   

#
# MAIN
#
if __name__ == '__main__':
   
    cr = cr2.CardRecognition()

    path = './test'
    '''
    for filename in os.listdir(path):
        print(filename)
        cards = cr.get_cards(os.path.join(path,filename), 4)
        print(cards)
    '''
    while True:
       filename = input('Enter Card Image: ')
       filename = os.path.join(path,filename)

       if os.path.isfile(filename):
           print(filename)
           cards = cr.get_cards(filename)
           print('Are these your cards?')
           print(cards)
           print('-------------------------------------------')
    
