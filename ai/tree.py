from board import *
from collections import defaultdict


class TreePlayer:
    def __init__(self, ID):
        self.ID = ID

    def deSymmetrize(self, board_state, moves, player_id):
        new_moves = []
        new_states = []
        for move in moves:
            b = Board(board_state)
            b.makeMove(move, player_id)
            already_in = False
            for i in range(len(new_moves)):
                state = b.getState()
                for _ in range(3):
                    state = Right90(state)
                    if state == new_states[i]:
                        already_in = True
                        break

                if already_in or new_states[i] == Transpose(b.getState()) or \
                        new_states[i] == ATranspose(b.getState()):
                    already_in = True
                    break

            if not already_in:
                new_moves.append(move)
                new_states.append(b.getState())

        return new_moves

    def getOpenMoves(self, board_state):
        open_moves = []
        for ri, row in enumerate(board_state):
            for ci, value in enumerate(row):
                if value is None:
                    open_moves.append((ri, ci))

        return open_moves

    def depthFirstExpand(self, state_node, player_index, player_ids):
        state = state_node.state
        curr_player = player_ids[player_index]
        avail_moves = self.deSymmetrize(state, self.getOpenMoves(state),
                                        curr_player)
        # Record "cats" games
        if len(avail_moves) == 0:
            state_node.updateWinner(None)

        for move in avail_moves:
            b = Board(state)
            b.makeMove(move, curr_player)

            new_node = TreeNode(state_node, b.getState())

            state_node.addMove(move, new_node)

            winner = b.getWinner()
            if winner is None:
                next_player_index = (player_index + 1) % len(player_ids)
                self.depthFirstExpand(new_node, next_player_index, player_ids)
            else:
                new_node.updateWinner(winner)


    def getMove(self, board_state, player_order):
        print(f"{self.ID} thinking...")
        root = TreeNode(None, board_state)

        self.depthFirstExpand(root, 0, player_order)
        move_ratios = []
        for move, new_state in root.next_moves.items():
            # Try W/L ratio
            my_wins = new_state.winners[self.ID] + new_state.winners[None]
            their_wins = new_state.winners[player_order[1]]
            # Potentially take a win right away
            if their_wins == 0:
                move_ratios = [(0, move, new_state.winners)]
                break
            else:
                wl = my_wins - their_wins
                move_ratios.append((wl, move, new_state.winners))

        move_ratios.sort(reverse=True)

        for move in move_ratios:
            print(f"\t{move[1]}: {move[0]:0.4f} {dict(move[2])}")

        return move_ratios[0][1]


class TreeNode:
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.next_moves = {}
        self.winners = defaultdict(int)

    def addMove(self, move, node):
        self.next_moves[move] = node

    def updateWinner(self, winner):
        self.winners[winner] += 1

        if self.parent:
            self.parent.updateWinner(winner)

    def __str__(self):
        return f"{self.state}{self.next_moves}"
