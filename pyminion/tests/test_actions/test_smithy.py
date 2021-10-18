from pyminion.models.base import Turn, Player
from pyminion.models.cards import Smithy
from pyminion.base_set.base_cards import smithy


def test_smithy_draw(turn: Turn, player: Player):
    """
    Create a hand with one smithy then play that smithy.
    Assert smithy on playmat, handsize increases to 3, action count goes to 0

    """
    player.hand.add(smithy)
    assert len(player.hand) == 1
    player.hand.cards[0].play(turn, player)
    assert len(player.hand) == 3
    assert type(player.playmat.cards[0]) is Smithy