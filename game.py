__all__ = ["Game"]


class Game:
    def __init__(self, players: list, board):
        self.players = players
        self.board = board

        self.player_index = 0

    def getPlayOrder(self):
        order = []
        index = self.player_index
        while len(order) < len(self.players):
            order.append(self.players[index].ID)
            index = (index + 1 ) % len(self.players)

        return order

    def update(self):
        move = self.players[self.player_index].getMove(self.board.getState(),
                                                       self.getPlayOrder())
        player_key = self.players[self.player_index].ID
        self.board.makeMove(move, player_key)
        self.player_index = (self.player_index + 1) % len(self.players)

    def play(self):
        print(self.board)
        while True:
            self.update()
            print(self.board)
            winner = self.board.getWinner()
            if winner is not None or not self.board.canMove():
                return winner
