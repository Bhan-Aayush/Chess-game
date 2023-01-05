from a2_game_tree import GameTree, GAME_START_MOVE


def build_sample_game_tree() -> GameTree:
    """Create an example game tree."""
    game_tree = GameTree(GAME_START_MOVE, True)

    game_tree.add_subtree(GameTree('a2b3', False))
    game_tree.add_subtree(GameTree('b2c3', False))
    game_tree.add_subtree(GameTree('b2a3', False))

    sub1 = GameTree('c2d3', False)
    sub2 = GameTree('d4d3', True)
    sub2.add_subtree(GameTree('d2c3', False))
    sub2.add_subtree(GameTree('b1d3', False))
    sub1.add_subtree(sub2)
    game_tree.add_subtree(sub1)

    game_tree.add_subtree(GameTree('c2b3', False))
    game_tree.add_subtree(GameTree('d2c3', False))

    return game_tree
