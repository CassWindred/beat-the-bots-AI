# DELETE LATER

import random as random
from enum import Enum


class Actions(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    DYNAMITE = 4
    WATERBOMB = 5


our_previous_moves = []
oppPreviousMoves = []

# END DELETE LATER


# dictionary mapping each action to the actions it wins against
winning_pairs = {Actions.ROCK: [Actions.SCISSORS, Actions.WATERBOMB], Actions.PAPER: [Actions.ROCK, Actions.WATERBOMB],
                 Actions.SCISSORS: [Actions.PAPER, Actions.WATERBOMB], Actions.DYNAMITE: [Actions.ROCK, Actions.PAPER, Actions.SCISSORS],
                 Actions.WATERBOMB: [Actions.DYNAMITE]}

# dictionary mapping each action to the actions it loses against
losing_pairs = {Actions.ROCK: [Actions.DYNAMITE, Actions.PAPER], Actions.PAPER: [Actions.SCISSORS, Actions.DYNAMITE],
                Actions.SCISSORS: [Actions.ROCK, Actions.DYNAMITE], Actions.DYNAMITE: [Actions.WATERBOMB],
                Actions.WATERBOMB: [Actions.ROCK, Actions.PAPER, Actions.SCISSORS]}

# keeps track of how often the AI's move abides by each condition
# might need to be reset on start??
opponent_decision_making = {
    "beat_opp_prev": 0, "beat_our_prev": 0, "lose_opp_prev": 0, "lose_our_prev": 0}

# compares the previous move of the opponent on turn x to;
# opponent's previous move
# our previous move
# identifies whether the opponent's algorithm is making decisions based on our/their past moves, NOT including repetition


def previous_moves_comparison(our_previous_moves, oppPreviousMoves):
    # remove the parameters when add function to application.py

    # checks the opponent's most recent move against both its and our previous moves, and increments the_opponent+decision_making dictionary appropriately
    if len(our_previous_moves) >= 1 and len(oppPreviousMoves) >= 2:
        opponents_last_move = oppPreviousMoves[-1]
        opponents_previous_move = oppPreviousMoves[-2]

        our_previous_move = our_previous_moves[-2]

        # does the opponent choose the action which would beat their previous move?
        if opponents_previous_move in winning_pairs[opponents_last_move]:
            opponent_decision_making["beat_opp_prev"] += 1

        # does the opponent choose the action which would beat our last move?
        if our_previous_move in winning_pairs[opponents_last_move]:
            opponent_decision_making["beat_our_prev"] += 1

        # does the opponent choose the action which would lose to their previous move?
        if opponents_last_move in winning_pairs[opponents_previous_move]:
            opponent_decision_making["lose_opp_prev"] += 1

        # does the opponent choose the action which would lose to our previous move?
        if opponents_last_move in winning_pairs[our_previous_move]:
            opponent_decision_making["lose_our_prev"] += 1

    # decides if there is enough evidence in opponent_decision_making to accurately predict their next move
    action = None

    beat_opp_prev_ratio = opponent_decision_making["beat_opp_prev"]/len(
        oppPreviousMoves)
    if beat_opp_prev_ratio > 0.5:
        action = random.choice(losing_pairs[opponents_last_move])

    beat_our_prev_ratio = opponent_decision_making["beat_our_prev"]/len(
        oppPreviousMoves)
    if beat_our_prev_ratio > 0.5:
        action = random.choice(losing_pairs[our_previous_move])

    lose_opp_prev_ratio = opponent_decision_making["lose_opp_prev"]/len(
        oppPreviousMoves)
    if lose_opp_prev_ratio > 0.5:
        action = random.choice(winning_pairs[opponents_last_move])

    lose_our_prev_ratio = opponent_decision_making["lose_our_prev"]/len(
        oppPreviousMoves)
    if lose_our_prev_ratio > 0.5:
        action = random.choice(winning_pairs[our_previous_move])

    if action:
        return action.value
    else:
        return None


def tests():
    print("Test 1")
    # opponent chooses action which would beat THEIR previous move
    our_previous_moves = [Actions.DYNAMITE, Actions.WATERBOMB]
    oppPreviousMoves = [Actions.PAPER, Actions.SCISSORS]
    previous_moves_comparison(our_previous_moves, oppPreviousMoves)

    print("Test 2")
    # opponent chooses action which would beat OUR previous move
    our_previous_moves = [Actions.DYNAMITE, Actions.WATERBOMB]
    oppPreviousMoves = [Actions.ROCK, Actions.WATERBOMB]
    print(previous_moves_comparison(our_previous_moves, oppPreviousMoves))

    print("Test 3")
    # opponent chooses action which would lose to THEIR previous move
    our_previous_moves = [Actions.DYNAMITE, Actions.WATERBOMB]
    oppPreviousMoves = [Actions.SCISSORS, Actions.WATERBOMB]
    print(previous_moves_comparison(our_previous_moves, oppPreviousMoves))

    print("Test 4")
    # opponent chooses action which would lose to OUR previous move
    our_previous_moves = [Actions.DYNAMITE, Actions.WATERBOMB]
    oppPreviousMoves = [Actions.SCISSORS, Actions.ROCK]
    print(previous_moves_comparison(our_previous_moves, oppPreviousMoves))

