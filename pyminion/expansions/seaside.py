import logging
from typing import TYPE_CHECKING, Any, List, Tuple

from pyminion.core import AbstractDeck, CardType, Action, Card, Treasure, Victory
from pyminion.effects import AttackEffect, EffectAction, FuncPlayerCardGameEffect, FuncPlayerGameEffect, PlayerGameEffect
from pyminion.exceptions import EmptyPile
from pyminion.game import Game
from pyminion.player import Player

if TYPE_CHECKING:
    from pyminion.game import Game


logger = logging.getLogger()


class BasicNextTurnEffect(PlayerGameEffect):
    def __init__(
            self,
            name: str,
            player: Player,
            card: Card,
            draw: int = 0,
            actions: int = 0,
            money: int = 0,
            buys: int = 0,
            discard: int = 0,
    ):
        super().__init__(name)
        self.player = player
        self.card = card
        self.draw = draw
        self.actions = actions
        self.money = money
        self.buys = buys
        self.discard = discard

        player.add_playmat_persistent_card(card)

    def get_action(self) -> EffectAction:
        if self.draw > 0 and self.discard > 0:
            return EffectAction.HandAddRemoveCards
        elif self.draw > 0:
            return EffectAction.HandAddCards
        elif self.discard > 0:
            return EffectAction.HandRemoveCards
        else:
            return EffectAction.Other

    def is_triggered(self, player: Player, game: "Game") -> bool:
        return player is self.player

    def handler(self, player: Player, game: "Game") -> None:
        if self.draw > 0:
            player.draw(self.draw)

        player.state.actions += self.actions
        player.state.money += self.money
        player.state.buys += self.buys

        if self.discard > 0 and len(player.hand) > 0:
            if len(player.hand) <= self.discard:
                discard_cards = player.hand.cards[:]
            else:
                discard_cards = player.decider.discard_decision(
                    prompt=f"Discard {self.discard} card(s) from your hand: ",
                    card=self.card,
                    valid_cards=player.hand.cards,
                    player=player,
                    game=game,
                    min_num_discard=self.discard,
                    max_num_discard=self.discard,
                )
                assert len(discard_cards) == self.discard

            for discard_card in discard_cards:
                player.discard(game, discard_card)

        player.remove_playmat_persistent_card(self.card)
        game.effect_registry.unregister_turn_start_effects(self.get_name(), 1)


class RemovePersistentMultiPlayEffect(PlayerGameEffect):
    def __init__(self, player: Player, card: Card):
        super().__init__("Remove Persistent Multi-Play Card")
        self.player = player
        self.card = card

    def get_action(self) -> EffectAction:
        return EffectAction.Other

    def is_triggered(self, player: Player, game: "Game") -> bool:
        return player is self.player

    def handler(self, player: Player, game: "Game") -> None:
        player.remove_playmat_persistent_card(self.card)
        game.effect_registry.unregister_turn_start_effects(self.get_name(), 1)


class Astrolabe(Treasure):
    """
    Now and at the start of your next turn:
    $1
    +1 Buy

    """

    def __init__(self):
        super().__init__("Astrolabe", 3, (CardType.Treasure, CardType.Duration), 1)

    def play(self, player: Player, game: "Game") -> None:
        player.playmat.add(self)
        player.hand.remove(self)
        player.state.money += self.money
        player.state.buys += 1

        effect = BasicNextTurnEffect(f"{self.name}: +$1, +1 Buy", player, self, money=1, buys=1)
        game.effect_registry.register_turn_start_effect(effect)


class Bazaar(Action):
    """
    +1 Card
    +2 Actions
    +$1

    """

    def __init__(self):
        super().__init__(name="Bazaar", cost=5, type=(CardType.Action,), draw=1, actions=2, money=1)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")

        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 2
        player.state.money += 1


class Caravan(Action):
    """
    +1 Card
    +1 Action

    At the start of your next turn, +1 Card.

    """

    def __init__(self):
        super().__init__(name="Caravan", cost=4, type=(CardType.Action, CardType.Duration), draw=1, actions=1)

    def play(
        self, player: Player, game: "Game", generic_play: bool = True
    ) -> None:

        logger.info(f"{player} plays {self}")
        if generic_play:
            super().generic_play(player)

        player.draw()
        player.state.actions += 1

        effect = BasicNextTurnEffect(f"{self.name}: +1 Card", player, self, draw=1)
        game.effect_registry.register_turn_start_effect(effect)

    def multi_play(self, player: Player, game: Game, multi_play_card: Card, state: Any, generic_play: bool = True) -> Any:
        count = 1 if state is None else int(state) + 1
        if count == 1:
            player.add_playmat_persistent_card(multi_play_card)
            effect = RemovePersistentMultiPlayEffect(player, multi_play_card)
            game.effect_registry.register_turn_start_effect(effect)

        super().multi_play(player, game, multi_play_card, state, generic_play)

        return count


astrolabe = Astrolabe()
bazaar = Bazaar()
caravan = Caravan()


seaside_set: List[Card] = [
    astrolabe,
    bazaar,
    caravan,
]
