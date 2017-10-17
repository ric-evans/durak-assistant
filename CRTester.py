

import CardRecognition as cr2
import os
        
#
# MAIN
#
if __name__ == '__main__':
   
    cr = cr2.CardRecognition()

    path = './test'

    while True:
       filename = input('Enter Card Image: ')
       
       if filename == '*':
           net_acc = []
           for filename in os.listdir(path):
               print(filename)
               cards, testnum, acc = cr.test_cards(os.path.join(path,filename))
               print(cards)
               for i in range(testnum):
                   net_acc.append(acc) 
               #print(acc)
               print('==== Cummulative Net Accuracy: {:.3f}% ===='.format(100*sum(net_acc)/len(net_acc)))
               print('-------------------------------------------')
       else:                            
           filename = os.path.join(path,filename)
           if os.path.isfile(filename):
               print(filename)
               cards = cr.get_cards(filename)
               print('Are these your cards?')
               print(cards)
       
       print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
           
