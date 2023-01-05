"""CSC111 Winter 2021 Assignment 2: Trees, Chess, and Artificial Intelligence (Part 3)

Instructions (READ THIS FIRST!)
===============================

This Python module contains the start of functions and/or classes you'll define
for Part 3 of this assignment. You should NOT make any changes to a2_minichess.py.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2022 Mario Badr, David Liu, and Isaac Waller.
"""
import random
from typing import Optional

import a2_game_tree
import a2_minichess


class ExploringPlayer(a2_minichess.Player):
    """A Minichess player that plays greedily some of the time, and randomly some of the time.

    See assignment handout for details.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[a2_game_tree.GameTree]
    _exploration_probability: float

    def __init__(self, game_tree: a2_game_tree.GameTree, exploration_probability: float) -> None:
        """Initialize this player."""
        self._game_tree = game_tree
        self._exploration_probability = exploration_probability

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
            return self.make_move_probability_helper(game)

    def make_move_probability_helper(self, game: a2_minichess.MinichessGame) -> str:
        """Helper for make_move, used to choose moves based on probability"""

        rand_float = random.uniform(0, 1)
        if rand_float >= self._exploration_probability:
            possible_moves = {}
            for x in self._game_tree.get_subtrees():
                possible_moves[x.white_win_probability] = x.move
            if self._game_tree.is_white_move:
                return possible_moves[max(possible_moves)]
            else:
                return possible_moves[max(possible_moves)]
        else:
            rand_choice = random.choice(game.get_valid_moves())
            existing_subtrees = self._game_tree.get_subtrees()
            if rand_choice in existing_subtrees:
                self._game_tree = None
            return rand_choice


def run_learning_algorithm(exploration_probabilities: list[float],
                           show_stats: bool = True) -> a2_game_tree.GameTree:
    """Play a sequence of Minichess games using an ExploringPlayer as the White player.

    This algorithm first initializes an empty GameTree. All ExploringPlayers will use this
    SAME GameTree object, which will be mutated over the course of the algorithm!
    Return this object.

    There are len(exploration_probabilities) games played, where at game i (starting at 0):
        - White is an ExploringPlayer (using the game tree) whose exploration probability
            is equal to exploration_probabilities[i]
        - Black is a RandomPlayer
        - AFTER the game, the move sequence from the game is inserted into the game tree,
          with a white win probability of 1.0 if White won the game, and 0.0 otherwise.

    Implementation note:
        - A NEW ExploringPlayer instance should be created for each loop iteration.
          However, each one should use the SAME GameTree object.
        - You should call run_game, NOT run_games, from a2_minichess. This is because you
          need more control over what happens after each game runs, which you can get by
          writing your own loop that calls run_game. However, you can base your loop on
          the implementation of run_games.
        - Note that run_game from a2_minichess returns both the winner and the move sequence
          after the game ends.
        - You may call print in this function to report progress made in each game.
        - Note that this function returns the final GameTree object. You can inspect the
          white_win_probability of its nodes, calculate its size, or and use it in a
          RandomTreePlayer or GreedyTreePlayer to see how they do with it.
    """
    # Start with a GameTree in the initial state
    game_tree = a2_game_tree.GameTree()

    # Play games using the ExploringPlayer and update the GameTree after each one
    results_so_far = []

    # Write your loop here, according to the description above.
    for x in exploration_probabilities:
        white = ExploringPlayer(game_tree, x)
        black = a2_minichess.RandomPlayer()

        a = a2_minichess.run_game(white, black, True, 6)

        results_so_far.append(a[0])

        if a[0] == 'White':
            game_tree.insert_move_sequence(a[1], 0, 1.0)
        else:
            game_tree.insert_move_sequence(a[1], 0, 0.0)

        # game_tree.add_subtree(run_learning_algorithm(exploration_probabilities, curr_game + 1))

    print(results_so_far)

    if show_stats:
        a2_minichess.plot_game_statistics(results_so_far)

    return game_tree


def part3_runner() -> a2_game_tree.GameTree:
    """Run example for Part 3.
    """
    probabilities = [0.0] * 10

    return run_learning_algorithm(probabilities)


