## DELETE LATER

from enum import Enum

class Actions(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    DYNAMITE = 4
    WATERBOMB = 5

winning_pairs = {Actions.ROCK:[Actions.SCISSORS, Actions.WATERBOMB], Actions.PAPER:[Actions.ROCK, Actions.WATERBOMB],
                Actions.SCISSORS:[Actions.PAPER, Actions.WATERBOMB], Actions.DYNAMITE:[Actions.ROCK, Actions.PAPER, Actions.SCISSORS],
                Actions.WATERBOMB:[Actions.DYNAMITE]}


