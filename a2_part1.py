
import csv
import random
from typing import Optional

import a2_game_tree
import a2_minichess


################################################################################
# Loading Minichess datasets
################################################################################
def load_game_tree(games_file: str) -> a2_game_tree.GameTree:
    """Create a game tree based on games_file.
    """
    game_tree = a2_game_tree.GameTree()
    with open(games_file) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            game_tree.insert_move_sequence(row, 0)

    return game_tree


################################################################################
# Minichess AI that uses a GameTree
################################################################################
class RandomTreePlayer(a2_minichess.Player):
    """A Minichess player that plays randomly based on a given GameTree.

    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]

    def __init__(self, game_tree: a2_game_tree.GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree

    def make_move(self, game: a2_minichess.MinichessGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        if self._game_tree is None or self._game_tree.find_subtree_by_move(previous_move) is None:
            self._game_tree = None
        else:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)

        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            return random.choice(game.get_valid_moves())
        else:
            possible_moves = []
            for x in self._game_tree.get_subtrees():
                possible_moves.append(x.move)
            return random.choice(possible_moves)


def part1_runner(games_file: str, n: int, black_random: bool) -> None:
    """Create a game tree from the given file, and run n games where White is a RandomTreePlayer.

    """
    new_game = load_game_tree(games_file)

    white = RandomTreePlayer(new_game)
    if black_random:
        black = a2_minichess.RandomPlayer()
    else:
        black = RandomTreePlayer(new_game)

    a2_minichess.run_games(n, white, black, True, 1, False)


