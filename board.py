from functools import reduce
from copy import copy


def AllSame(items):
    last = items[0]
    for item in items:
        if last != item:
            return False

    return last


class Board:
    def GetNewBoard():
        return [[None] * 3 for _ in range(3)]

    def CopyState(state):
        return state and [copy(row) for row in state]


    def __init__(self, initial_state=None):
        self._state = Board.CopyState(initial_state) or Board.GetNewBoard()

    def getState(self):
        return [copy(row) for row in self._state]

    def canMove(self):
        # True if there is None in any row
        return any([None in r for r in self._state])

    def _getCol(self, i):
        return [r[i] for r in self._state]

    def _getDiag(self, offset=0, factor=1):
        return [self._state[i][offset + factor * i] for i in range(3)]

    def getWinner(self):
        for i in range(3):
            r_key = AllSame(self._state[i])
            c_key = AllSame(self._getCol(i))
            key = r_key or c_key
            if key != False:
                return key

        d1 = AllSame(self._getDiag())
        d2 = AllSame(self._getDiag(2, -1))
        key = d1 or d2
        if key != False:
            return key

        return None

    def makeMove(self, position, player_key):
        row, col = position
        if self._state[row][col] is None:
            self._state[row][col] = player_key

    def __str__(self, mapping=None):
        if mapping is None:
            mapping = {1: "x", 2: "o", None: " "}

        s = []
        for i in range(3):
            row = self._state[i]
            s.append("{}|{}|{}".format(*list(map(lambda x: mapping[x], row))))
            if i != 2:
                s.append("-+-+-")

        return "\n".join(s)

