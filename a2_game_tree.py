from __future__ import annotations
from typing import Optional

GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Minichess moves.

    Each node in the tree stores a Minichess move and a boolean representing whether
    the current player (who will make the next move) is White or Black."""
    move: str
    is_white_move: float
    white_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, move: str = GAME_START_MOVE,
                 is_white_move: bool = True, white_win_probability: Optional[float] = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        >>> game.is_white_move
        True
        """
        self.move = move
        self.is_white_move = is_white_move
        self._subtrees = []
        self.white_win_probability = white_win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_white_move:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"
        move_desc = f'{self.move} -> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    ############################################################################
    # Part 1: Loading and "Replaying" Minichess games
    ############################################################################
    def insert_move_sequence(self, moves: list[str], bw: int,
                             white_new_leaf_win_probability: Optional[float] = 0.0) -> None:
        """Insert the given sequence of moves into this tree."""

        actual_moves = moves

        if actual_moves == []:
            return None
        else:
            needed_subtree = None
            for subtree in self._subtrees:
                if subtree.move == actual_moves[0]:
                    subtree.is_white_move = bool(bw % 2)
                    needed_subtree = subtree
                    break

            if needed_subtree is None:
                needed_subtree = GameTree(actual_moves[0])
                needed_subtree.is_white_move = bool(bw % 2)
                needed_subtree.white_win_probability = white_new_leaf_win_probability
                self.add_subtree(needed_subtree)

            actual_moves.reverse()
            needed_subtree.insert_move_sequence(insert_move_sequence_helper(actual_moves),
                                                bw + 1)

        return None

    ############################################################################
    # Part 2: Complete Game Trees and Win Probabilities
    ############################################################################
    def _update_white_win_probability(self) -> None:
        """Recalculate the white win probability of this tree.
        """

        if self._subtrees == []:
            return None
        elif self._subtrees != [] and self.is_white_move:
            self.white_win_probability = sum([x.white_win_probability for x in self._subtrees])
            return None
        else:
            self.white_win_probability = int((sum(x.white_win_probability for x in self._subtrees))
                                             / len([x.white_win_probability for x in
                                                    self._subtrees]))
            return None


def insert_move_sequence_helper(moves: list[str]) -> list[str]:
    """Helper function for insert_move_sequence"""

    if moves == []:
        return []
    else:
        current_list = moves
        current_list.pop(-1)
        current_list.reverse()
        return current_list
