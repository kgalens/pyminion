from pyminion.expansions.base import workshop
from pyminion.game import Game
from pyminion.players import Human


def test_workshop_gain_valid(human: Human, game: Game, monkeypatch):
    human.hand.add(workshop)
    assert len(human.discard_pile) == 0

    # mock decision = input() as "Copper" to discard
    monkeypatch.setattr("builtins.input", lambda _: "Estate")

    human.hand.cards[0].play(human, game)
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1
    assert human.state.actions == 0
    assert human.discard_pile.cards[0].name == "Estate"
    assert len(game.supply.piles[3]) == 4
