from pydealer import *
import random
random.seed(13453)
class Game:
    
    def __init__(self) -> None:        
        self.OPEN = 'open'
        self.DECK = 'deck'
        #shuffle deck
        self.deck = Deck()
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
        
        # change playerTurn
        self.playerTurn = (self.playerTurn+1)%2
        
        return c
    
    def checkMeld(self,meld:Stack):
        #if meld size is less than 3 it is invalid
        if meld.size <3: return 0 #0 means invalid
        #sort cards
        meld.sort()
        #get the different suits in the meld
        suits = set()
        for c in meld:
            suits.add(c.suit)  
             
        #check if meld is first life, second life, or set in that order
        
        def checkFirstLife():
            #if there is only 1 suit check if it is a first life
            if len(suits)==1:
                #convert card values to numbers from 1 to 13 (2 to Ace)
                meldVals = [DEFAULT_RANKS["values"][c.value] for c in meld]
                meldVals.sort()
                
                def checkSeq(vals):
                    mVals = vals.copy()
                    val = mVals[0]
                    for i in mVals:
                        if val!=i:
                            return False
                        else:
                            val+=1
                    return True
                # Set Ace value to 0 for Ace-2-3 sequences
                meldVals2 = [i if i!=13 else 0 for i in meldVals]
                meldVals2.sort()
                #if either Ace being 0 or 13 makes a valid sequence then return True
                return checkSeq(meldVals) or checkSeq(meldVals2)
        if checkFirstLife(): return 1
        
        def checkSecondLife():
            meld2 = Stack()
            meld2.add(meld)
            
            #check how many jokers there are
            j = meld2.get(self.joker.value)
            
            # if meld is empty and there are 3 or more jokers return True
            if meld2.size==0 and len(j)>=3: return True
            meldVals = [DEFAULT_RANKS["values"][c.value] for c in meld2]
            #If there is more than 1 suit in the non joker cards return false
            suits2 = set()
            for c in meld2:
                suits2.add(c.suit)
            if len(suits2)>1: return False
            #check if it is second life
            def checkSeqWJoker(vals):
                numJokers = len(j)
                mVals = vals.copy()
                val = mVals[0]
                while len(mVals)>0:
                    if val == mVals[0]:
                        mVals.pop(0)
                        if len(mVals)==0:
                            return True
                    else:
                        if numJokers==0: return False
                        numJokers-=1
                    val+=1
                return True
            
            #set value of Ace to be 0 for Ace-2-3 sequences
            meldVals2 = [i if i!=13 else 0 for i in meldVals]
            meldVals2.sort()
            
            #if either Ace being 0 or 13 makes a valid sequence then return True
            return checkSeqWJoker(meldVals) or checkSeqWJoker(meldVals2)
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
        if checkSet(): return 3
        
        # if meld is none of the above return 0
        return 0

    def checkShow(self,melds:list):
        # if total number of cards is not 13 return false
        if sum([m.size for m in melds]) != 13:
            return False
        
        # get a list of meld types (first, second, or set)
        l = []
        for meld in melds:
            meldVal = self.checkMeld(meld)
            if meldVal ==0:
                return False
            l.append(meldVal)
        if 1 not in l: return False
        if 3 in l and l.count(1)+l.count(2)<2: return False
        return True
    
