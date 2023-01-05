
import random
from typing import Optional

import a2_game_tree
import a2_minichess


def generate_complete_game_tree(root_move: str, game_state: a2_minichess.MinichessGame,
                                d: int) -> a2_game_tree.GameTree:
    """Generate a complete game tree of depth d for all valid moves from the current game_state. """

    return_tree = a2_game_tree.GameTree(root_move)
    return_tree.is_white_move = game_state

    if d < 0 or game_state.get_winner() is not None:
        if game_state.get_winner() == "White":
            return_tree.white_win_probability = 1.0
        return return_tree

    else:
        counter_list = game_state.get_valid_moves()
        # main_subtree_list = []
        for x in counter_list:
            subtree_list = []
            new_move_tree = a2_game_tree.GameTree(x)
            return_tree.add_subtree(new_move_tree)
            new_game_state = game_state.copy_and_make_move(new_move_tree.move)

            subtree_list.append(generate_complete_game_tree(new_move_tree.move, new_game_state,
                                                            d - 1))
            # for y in subtree_list:
            #     return_tree.add_subtree(y)
            for y in return_tree.get_subtrees():
                add_subtree_to_subtrees(subtree_list, y, new_move_tree)
            # main_subtree_list.append
        return return_tree
        # return generate_complete_game_tree_helper(subtree_list, 0)

class GreedyTreePlayer(a2_minichess.Player):
    """A Minichess player that plays greedily based on a given GameTree.

    See assignment handout for description of its strategy.
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
        if previous_move is not None and self._game_tree is not None:
            self._game_tree = self._game_tree.find_subtree_by_move(previous_move)
            # Pick Move then update subtree
        if self._game_tree is None or self._game_tree.get_subtrees() == []:
            possible_moves = game.get_valid_moves()
            return random.choice(possible_moves)
        else:
            subtrees = self._game_tree.get_subtrees()
            if self._game_tree.is_white_move:
                highest_win_tree = subtrees[0]
                for subtree in subtrees:
                    if subtree.white_win_probability > highest_win_tree.white_win_probability:
                        highest_win_tree = subtree
                self._game_tree = highest_win_tree
                return highest_win_tree.move
            else:
                lowest_win_tree = subtrees[0]
                for subtree in subtrees:
                    if subtree.white_win_probability < lowest_win_tree.white_win_probability:
                        lowest_win_tree = subtree
                self._game_tree = lowest_win_tree
                return lowest_win_tree.move


def part2_runner(d: int, n: int, white_greedy: bool) -> None:
    """Create a complete game tree with the given depth, and run n games where
    one player is a GreedyTreePlayer and the other is a RandomPlayer.
    """
    game_state = a2_minichess.MinichessGame()
    complete_game_tree = generate_complete_game_tree('*', game_state, d)

    if white_greedy:
        white_player = GreedyTreePlayer(complete_game_tree)
        black_player = a2_minichess.RandomPlayer()
    else:
        white_player = a2_minichess.RandomPlayer()
        black_player = GreedyTreePlayer(complete_game_tree)
    a2_minichess.run_games(n, white_player, black_player, True, show_stats=True)


