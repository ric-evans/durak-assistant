'''
Eric Evans 

a simple Card object with a rank and suit
'''

SUITS = {'C','S','H','D'}
VALUE = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '\
9':9, 'X':10, 'J':11, 'Q':12, 'K':13, 'A':14}


class Card:
    
    rank = 'X'
    suit = 'C'
    
    def __init__(self,rank,suit):
        if suit[0].capitalize() not in SUITS:
            raise Exception('{} is not a valid suit'.format(suit))
        else:
            self.suit = suit[0].capitalize()

        if rank.capitalize() not in VALUE.keys():
            raise Exception('{} is not a valid rank'.format(rank))
        else:
            self.rank = rank.capitalize()

    
    def __getitem__(self,key):
        return self._list()[key]

    def __repr__(self):
        return 'Card{}'.format(self._list())

    def __str__(self):
        return self.__repr__()
    
    def _list(self):
        return (self.rank,self.suit)

    def value(self):
        return VALUE[self.rank]
