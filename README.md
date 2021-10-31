# Pyminion

Pyminion is a library for executing and analyzing games of [Dominion](https://www.riograndegames.com/games/dominion/). At its core, pyminion implements the rules and logic of Dominion and provides an API to interact with the game engine. In addition, it enables interactive games through the command line and simulation of games between bots.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Support](#support)
-   [Contributing](#contributing)

## Getting Started

Pyminion requires Python 3.8 and can easily be installed through pypi

```
python3 -m pip install pyminion
```

## Usage

To play a game against a bot through the command line:

```python
from pyminion.expansions.base import start_cards, core_supply, kingdom_cards
from pyminion.players import BigMoney, Human, Deck
from pyminion.models.core import Game, Supply

# Initialize player and bot
human = Human(deck=Deck(start_cards))
bot = BigMoney(deck=Deck(start_cards))

# Setup the game
supply = Supply(piles=core_supply + kingdom_cards)
game = Game(players=[bot, human], supply=supply)

# Play game
game.start()
while not game.is_over():
    bot.take_turn(game)
    human.take_turn(game)
print("Winner: ", game.get_winner()

```

## Support

Please [open an issue](https://github.com/evanofslack/pyminion/issues/new) for support.

## Contributing

The most welcome contributions would be to add more cards from the base set of Dominion or to create new bots that perform better than basic big money strategy. Check the [open issues](https://github.com/evanofslack/pyminion/issues) to get a sense of what of is currently being worked on.

If you would like to contribute, please create a branch, add commits, and [open a pull request](https://github.com/evanofslack/pyminion/pulls).
