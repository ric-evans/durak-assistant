'''
Author - Eric Evans

This module handles game logic for the card game Durak, 
from a player's perspective.
Cards are 2-element tuple like ('5','H') (the five of hearts).
-- 10 is 'X'

- PlayRecommender is the main class that deals with the current 
game context (the player's hand, community cards, trump suit)

- CardComparator is a helper class that deals with context-free 
(excluding the trump suit) operations that need card comparisons.

''' 

import Card


#
# Given the trump suit, hand cards, and community cards,
# recommend a plays for attacking or defending
#
class PlayRecommender(object):

    hand = None
    comm = None
    card_comp = None
    
    
    def __init__(self,trump):
        if type(trump) is str and trump[0] in Card.SUITS: 
            self.card_comp = CardComparator(trump)
        else:
            raise Exception('{} is not a legal suit'.format(trump[0]))
        

    # sort and set hand 
    def _set_hand(self,cards):
        if cards:
            self.hand = self.card_comp.sort(cards)
        else:
            self.hand = None
        
        
    # sort and set comm
    def _set_community(self,cards):
        if cards:
            self.comm = self.card_comp.sort(cards)
        else:
            self.comm = None


    #
    # clear hand cards
    #
    def reset_hand(self):
        self._set_hand(None)


    #
    # clear community cards
    #
    def reset_community(self):
        self._set_community(None)
        

    #
    # add additions to hand
    #
    def add_to_hand(self,cards):
        if self.hand:
            set_list = list( set(self.hand + cards) )
            self._set_hand(set_list)
        else:
            self._set_hand(cards)


    #
    # add additions to comm
    #
    def add_to_community(self,cards):
        if self.comm:
            set_list = list( set(self.comm + cards) )
            self._set_community(set_list)
        else:
            self._set_community(cards)

    #
    # remove card from hand
    #
    def remove_from_hand(self,card):
        if self.hand and card in self.hand:
            self.hand.remove(card)

            
    #
    # remove card from comm
    #
    def remove_from_community(self,card):
        if self.comm and card in self.comm:
            self.comm.remove(card)

            
    #
    # return attack_advice() where all attacks have
    # the same rank as a community card
    #
    def additional_attack_advice(self):
        if not self.hand or not self.comm:
            return None
        
        addtl_attacks = []
        attacks = self.attack_advice()
        for attk_cards in attacks: # attk_cards -> list of cards
            for comm_card in self.comm: # comm_card -> a card
                if self.card_comp.same_rank(attk_cards[0], comm_card):
                    addtl_attacks.append(attk_cards)
                    break
        return addtl_attacks
        
            
    #
    # return a {'pass': [(card_pass),...],
    #           'defend': [ ( (card_defend),(card_comm) ),... ] }
    # of best defense moves
    #
    def defend_advice(self,include_unbeatables=False):
        if not self.hand or not self.comm:
            return None

        if len(self.hand) < len(self.comm):
            raise Exception('You cannot get attacked with more cards than you have in your hand')
        
        play = {}
        
        # 1st: pass play? 
        passable, pass_cards = self._get_passes()
        if passable:
            play['pass'] = pass_cards
  
        # 2nd: defend?
        defendable, defends = self._get_defenses()
        if defendable or include_unbeatables:
            play['defend'] = defends

        winnable = passable or defendable
        return winnable, play


    # return bool(if completely defendable) and
    # [ ( (card_defend),(card_comm) ),... ] of all comm cards
    # that are beat by a hand card (or "None" if unbeatable)
    def _get_defenses(self):
        defendable = True
        defends = []
        non_trumps, trumps = self.card_comp.split_out_trumps(self.hand)
        for cm in self.comm:
            #print(cm)
            found = False
            # search among non-trump cards
            for ntc in non_trumps:
                if self.card_comp.does_beat(ntc, cm):
                    defends.append( (ntc,cm) )
                    non_trumps.remove(ntc)
                    found = True
                    break
            if found: continue
            # search among trump cards
            for tc in trumps:
                if self.card_comp.does_beat(tc, cm):
                    defends.append( (tc,cm) )
                    trumps.remove(tc)
                    found = True
                    break
            # see if a defending card is possible
            if not found:
                defends.append( ("None",cm) )
                defendable = False

        return defendable, defends 
            
        
        
    # return bool(if passable) and lowest value card from hand that
    # has a matching rank of a community card
    def _get_passes(self):
        passes = []
        for card in self.hand:
            for cm in self.comm:
                if self.card_comp.same_rank(card,cm):
                    passes.append(card)
                    break
        return bool(passes), passes
            
    
    #
    # return a [ [ (card),... ],... ] of possible attacks
    # in best play order
    #
    def attack_advice(self):
        if self.hand:
            return self.card_comp.group_up(self.hand)
        else:
            return None

    
#
# For operations that require comparing card values
#
class CardComparator(object):

    trump = None
    
    def __init__(self,trump):
        self.trump = trump


    # True if card is a trump card
    def is_trump_card(self,card):
        #print('{} vs. {}'.format(card[1][0], self.trump))
        return card.suit == self.trump


    # True if cards have same rank
    def same_rank(self, a, b):
        return a.rank == b.rank

    
    # True if cards have same suit
    def same_suit(self, a, b):
        return a.suit == b.suit


    # True if a beats b
    def does_beat(self, me, you):
        # check if same rank (and me is not trump)
        if self.same_rank(me, you) and not self.is_trump_card(me):
            return False #change to True for multi-deck same card beat

        # check if cards are the same suit (and me is not trump)
        if not self.same_suit(me, you) and not self.is_trump_card(me):
            return False
            
        ordered = self.sort( [me,you] )
        return ordered[0] == you

        
    # sorting key
    def _key_group_by_rank(self,group): 
        return ( group[0].value() , len(group) )

    
    #
    # group up by rank
    # groups sorted by rank in preference of
    #  1) groups w/o a trump
    #  2) single non-trump cards
    #  3) groups w/ a trump
    #  4) single trump cards
    #
    def group_up(self, cds):
        groups = []
        
        # add card groups w/ or w/o trumps to groups
        for card in cds:
            # check if card is already in its group
            skip = False
            for gp in groups:
                if card in gp:
                    skip = True
            # make new group
            if not skip:
                gp = [ cd for cd in cds if self.same_rank(cd,card) ]
                if len(gp) > 1:
                    groups.append(gp)

        # get non-trump group and trump group from groups
        non_trump_groups = []
        trump_groups = []
        for gp in groups:
            # remove trump-cards from gp
            #non_tgp = [ cd for cd in gp if not self.is_trump_card(cd) ]
            non_tgp, _ = self.split_out_trumps(gp)
            # add non-trumps if there a multiple cards still
            if len(non_tgp) > 1: 
                non_trump_groups.append(non_tgp)
            # check if there were trumps in gp
            if len(non_tgp) != len(gp): 
                trump_groups.append(gp)
                
        # get non-trump single cards and trump single cards
        non_trump_singles, trump_singles = self.split_out_trumps(cds)
        # make into group of 1 -- one man wolfpack
        non_trump_singles = [ [cd] for cd in non_trump_singles ]
        trump_singles = [ [cd] for cd in trump_singles]

        # sort each group-list
        non_trump_groups = sorted(non_trump_groups, key=self._key_group_by_rank)
        non_trump_singles = sorted(non_trump_singles, key=self._key_group_by_rank)
        trump_groups = sorted(trump_groups, key=self._key_group_by_rank)
        trump_singles = sorted(trump_singles, key=self._key_group_by_rank)
        
        return non_trump_groups + non_trump_singles + trump_groups + trump_singles
        

    # sorting key
    def _key_card_by_rank_then_suit(self,card):
        if self.is_trump_card(card):
            suit_val = 'Z' # inflated trump suit value
        else:
            suit_val = card.suit
        return (card.value(), suit_val)


    #
    # return 2 lists: non-trump cards and trump cards 
    #
    def split_out_trumps(self,cards):
        non_trumps = []
        trumps = []
        for card in cards:
            if self.is_trump_card(card):
                trumps.append(card)
            else:
                non_trumps.append(card)
        return non_trumps, trumps
    
    
    #
    # sort cards in rank_val order with all trump cards (sorted) at the end
    #
    def sort(self, cds, desc=False):
        # 1st: sort on rank_val
        cards = sorted(cds, key=self._key_card_by_rank_then_suit)

        # 2nd: pull out trump cards
        non_trumps, trumps = self.split_out_trumps(cards)

        #print(trumps)
        #print(non_trumps)
                
        # 3rd: union trumps and non-trumps
        ret = non_trumps + trumps

        # 4th: check desc and return
        if desc:
            return ret.reverse()
        else:
            return ret
                
