from pydealer import *
import Game

game = Game.Game()
h:Stack = game.hands[0]
h.sort()
# print("JOKER")
# print(game.joker)
# print()
# print("HAND")
# print(*h,sep=", ")
# print("MELD")

tempLife = Stack() + [Card(2,"Spades"),Card(3,"Spades"),Card(4,"Spades"),Card(5,"Spades")]
print(game.checkMeld(tempLife))

tempSet = Stack() + [Card(4,"Spades"),Card(4,"Hearts"),Card(4,"Clubs"),Card(10,"Spades")]
# print(game.checkMeld(tempSet))
