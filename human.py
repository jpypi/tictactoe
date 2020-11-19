import time
import sys

from board import *
from ai.tree import *


__all__ = ["Human", "TotalNodes", "LeafNodes", "ExploreActionTree"]


class Human:
    def __init__(self, ID):
        self.ID = ID

    def canMove(self, state, position):
        row, col = position
        try:
            if state[row][col] is None:
                return True
            else:
                return False
        except IndexError:
            return False

    def getMove(self, board_state, player_order):
        while True:
            argument = input("> ")
            if len(argument) == 0: continue
            if argument.strip().lower() == "q":
                sys.exit()

            move = tuple(map(lambda x: int(x.strip()), argument.split(",")))
            if self.canMove(board_state, move):
                return move
            else:
                print(f"Cannot place marker at: {move}. Invalid move.")


def TotalNodes(node):
    return len(node.next_moves) + \
            sum((TotalNodes(n) for n in node.next_moves.values()))


def LeafNodes(node):
    if not node.next_moves:
        return 1
    else:
        return sum(LeafNodes(n) for n in node.next_moves.values())


def ExploreActionTree():
    b = Board()
    p = TreePlayer(1)

    print("Building move tree...")
    start = time.time()
    root = TreeNode(None, b.getState())
    p.depthFirstExpand(root, 0, [1, 2])
    print(f"Elapsed time: {time.time() - start}")

    print("Calculating node stats...")
    print(f"Total nodes: {TotalNodes(root)}")
    print(f"Leaf nodes: {LeafNodes(root)}")

    current = root
    while True:
        print(Board(current.state))
        print(list(current.next_moves.keys()))
        raw_action = input("> ")
        if len(raw_action) == 0: continue

        action = raw_action[0]
        argument = raw_action[1:]

        if action == "q":
            break
        if action == "c":
            move = tuple(map(lambda x: int(x.strip()), argument.split(",")))
            current = current.next_moves[move]
        if action == "w":
            print("Wining paths:")
            print(dict(current.winners))
        if action == "p":
            if current.parent is None:
                print("This is the root node")
            else:
                count = 1
                if len(argument) > 0 and AllSame(argument) == "p":
                    count += len(argument)
                for i in range(count):
                    current = current.parent

