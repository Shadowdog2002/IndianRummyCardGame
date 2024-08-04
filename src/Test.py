from pydealer import *
from Game import Game
import random
random.seed(13453)
game = Game()
h:Stack = game.hands[0]
h.sort()
# print("JOKER")
# print(game.joker)
# print()
# print("HAND")
# print(*h,sep=", ")
# print("MELD")

tempLife = Stack() + [Card("Jack","Spades"),Card("King","Spades"),Card("Queen","Spades"),Card("Ace","Spades")]
assert game.checkMeld(tempLife)==1

tempSecondLife = Stack() + [Card(2,"Hearts"),Card(10,"Spades"),Card(4,"Hearts"),Card(5,"Hearts")]
assert game.checkMeld(tempSecondLife)==2
tempSecondLife = Stack() + [Card("10","Hearts"),Card(10,"Spades"),Card("10","Hearts")]
assert game.checkMeld(tempSecondLife)==2

tempSet = Stack() + [Card(4,"Spades"),Card(4,"Hearts"),Card(10,"Spades")]
assert game.checkMeld(tempSet)==3

assert game.checkShow([tempLife,tempSet,tempSet,tempSecondLife]) == True
print("All Tests Passed!")
