import pydealer
from pydealer import (Stack,Deck,Card)
import pydealer.card
from pydealer.const import (DEFAULT_RANKS)
import pydealer.stack
import pydealer.tools

import random
random.seed(13453)
class Game:
    def __init__(self) -> None:
        self.OPEN = 'open'
        self.DECK = 'deck'
        #shuffle deck
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        
        #deal hands
        self.hands = []
        self.hands.append(self.deck.deal(13))
        self.hands.append(self.deck.deal(13))
        
        #get jocker
        self.joker = self.deck.random_card(True)
        
        #choose open card
        self.openCards = Stack()
        self.openCards.add(self.deck.deal(1))
        
        #set player turn
        self.playerTurn = 0
    
    def draw(self,player,where = 'deck'):
        """
        Draw a card from arg:where and place it in arg:player's hand

        :arg int player:
            player number.

        :arg str where:
            Where to draw from, "deck" for deck or "open" for openCards.

        :returns:
            Card drawn
        """
        if player<0 or player>=len(self.hands):
            print("Player number out of bounds")
            raise IndexError
        if where==self.DECK:
            if self.deck.size == 0:
                topCard = self.openCards.deal(1)
                self.deck, self.openCards = self.openCards,topCard
                self.deck.shuffle()
                
            c = self.deck.deal(1)
            self.hands[player]+= c
        elif where == self.OPEN:
            if self.openCards.size==0:
                print("Invalid Draw From Open Cards")
                raise IndexError
            c = self.openCards.deal(1)
            self.hands[player]+= c
        else:
            print("draw method: invalid argument for where:",where)
            raise AttributeError
        return c

    def discard(self,player:int,card:Card):
        """
        Discards player's card at cardIndex.

        :arg int player:
            player number.

        :arg Card card:
            Card to remove from player hand.

        :returns:
            Card removed

        """
        if(card not in self.hands[player]):
            print("Discard Error: Player does not have: ",c)
            raise LookupError
        c = self.hands[player].get(str(card))
        self.openCards.add(c)
        return c
    
    def checkMeld(self,meld:Stack):
        #if meld size is less than 3 it is invalid
        if meld.size <3:
            return 0 #0 means invalid
        #sort cards
        meld.sort()
        #get the different suits in the meld
        suits = set()
        for c in meld:
            suits.add(c.suit)   
        #convert card values to numbers from 1 to 13 (2 to Ace)
        meldVals = [DEFAULT_RANKS["values"][c.value] for c in meld]
        def checkFirstLife():
            #if there is only 1 suit check if it is a first life
            if len(suits)==1:
                def checkSeq():
                    for i in range(0,len(meldVals)-1):
                        if not meldVals[i]+1 == meldVals[i+1]:
                            return False
                    return True
                return checkSeq()
        if checkFirstLife(): return 1
        
        def checkSecondLife():
            meld2 = Stack()
            meld2.add(meld)
            suits2 = set()
            
            #check how many jokers there are
            j = meld2.get(self.joker.value)
            meldVals = [DEFAULT_RANKS["values"][c.value] for c in meld2]
            
            #If there is more than 1 suit in the non joker cards return false
            for c in meld2:
                suits2.add(c.suit)
            if len(suits2)>1: return False
            #check if it is second life
            def checkSeqWJoker():
                numJokers = len(j)
                return False
            
            return checkSeqWJoker()
        if checkSecondLife(): return 2
        
        def checkSet():
            meld2 = Stack()
            meld2+=meld
            # get and remove jokers from meld
            j = meld2.get(self.joker.value)
            # if meld is empty and there are 3 or more jokers return True
            if meld2.size==0 and len(j)>=3: return True
            
            # if the values of the meld are different return False
            if not len(meld2.find(meld2[0].value))==meld2.size: return False
            
            # if there are any duplicate suits return false
            if not len(set([c.suit for c in meld2]))==meld2.size: return False
            
            
            return True
        if checkSet():
            return 3
        
        return 0
