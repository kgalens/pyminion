from pyminion.core import DeckCounter
from pyminion.expansions.base import curse, throne_room
from pyminion.expansions.seaside import Sailor, bazaar, fishing_village, seaside_set, sailor
from pyminion.game import Game
from pyminion.human import Human
from pyminion.player import Player
import pytest


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_trash(multiplayer_game: Game, monkeypatch):
    responses = ["y", "curse"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 4
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Curse"
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_no_trash(multiplayer_game: Game, monkeypatch):
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 5
    assert len(multiplayer_game.trash) == 0
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([sailor])
def test_sailor_one_card_trash(multiplayer_game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]

    while len(human.hand) > 0:
        human.hand.cards.pop()
    while len(human.deck) > 0:
        human.deck.cards.pop()
    while len(human.discard_pile) > 0:
        human.discard_pile.cards.pop()

    human.deck.add(curse)

    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)
    assert len(human.playmat) == 1
    assert type(human.playmat.cards[0]) is Sailor
    assert human.state.actions == 1
    assert human.state.money == 0
    assert human.playmat_persist_counts[sailor.name] == 1
    assert "Sailor: Trash card" in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)

    human.start_cleanup_phase(multiplayer_game)
    human.end_turn(multiplayer_game)

    human.start_turn(multiplayer_game)

    assert len(responses) == 0
    assert human.state.money == 2
    assert len(human.hand) == 0
    assert len(multiplayer_game.trash) == 1
    assert multiplayer_game.trash.cards[0].name == "Curse"
    assert human.playmat_persist_counts[sailor.name] == 0
    assert "Sailor: Trash card" not in (e.get_name() for e in multiplayer_game.effect_registry.turn_start_effects)


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([bazaar, fishing_village, sailor])
def test_sailor_play(multiplayer_game: Game, monkeypatch):
    responses = ["y"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)

    # ensure gaining a non-duration card will not be played
    human.gain(bazaar, multiplayer_game)
    assert len(responses) == 1
    assert len(human.playmat) == 1
    assert len(human.discard_pile) == 1

    # gain a duration card and play it
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 2
    assert human.playmat.cards[0].name == "Sailor"
    assert human.playmat.cards[1].name == "Fishing Village"
    assert len(human.discard_pile) == 1
    assert human.state.actions == 3
    assert human.state.money == 1

    # ensure gaining another duration card will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 2
    assert len(human.discard_pile) == 2


@pytest.mark.expansions([seaside_set])
@pytest.mark.kingdom_cards([fishing_village, sailor])
def test_sailor_no_play(multiplayer_game: Game, monkeypatch):
    responses = ["n"]
    monkeypatch.setattr("builtins.input", lambda _: responses.pop(0))

    human = multiplayer_game.players[0]
    human.hand.add(sailor)

    human.play(sailor, multiplayer_game)

    # ensure gained duration card will not be played
    human.gain(fishing_village, multiplayer_game)
    assert len(responses) == 0
    assert len(human.playmat) == 1
    assert human.playmat.cards[0].name == "Sailor"
    assert len(human.discard_pile) == 1
    assert human.discard_pile.cards[0].name == "Fishing Village"
