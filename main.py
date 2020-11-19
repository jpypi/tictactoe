#!/usr/bin/env python3


from board import *
from ai.tree import *
from game import Game
from human import *


if __name__ == "__main__":
    b = Board()
    p1 = TreePlayer(1)
    #p2 = TreePlayer(2)
    p2 = Human(2)

    g = Game([p1, p2], b)
    winner = g.play()
    print(f"Winner is: {winner}")

    #ExploreActionTree()
