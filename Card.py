


SUITS = {'C','S','H','D'}
VALUE = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '\
9':9, 'X':10, 'J':11, 'Q':12, 'K':13, 'A':14}


class Card:
    
    rank = 'X'
    suit = 'C'

    def __init__(self,rank,suit):
        self.rank = rank[0]
        self.suit = suit[0]
    
    def __getitem__(self,key):
        return self._list()[key]

    def __repr__(self):
        return 'Card{}'.format(self._list())
    
    def _list(self):
        return (self.rank,self.suit)

    def value(self):
        return VALUE[self.rank]
