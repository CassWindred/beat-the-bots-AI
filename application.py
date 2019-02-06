from flask import Flask, make_response
from enum import Enum
from flask_restful import reqparse, Api, Resource, abort
import random

# Create webserver
bot = Flask(__name__)

# API
api = Api(bot)

# API Arguments
parser = reqparse.RequestParser()
parser.add_argument('lastOpponentMove')
parser.add_argument('opponentName')
parser.add_argument('pointsToWin', type=int)
parser.add_argument('maxRounds', type=int)
parser.add_argument('dynamiteCount', type=int)

# dictionary mapping each action to the actions it wins against


# keeps track of how often the AI's move abides by each condition
opponent_decision_making = {
    "beat_opp_prev": 0, "beat_our_prev": 0, "lose_opp_prev": 0, "lose_our_prev": 0}

# Game state
class GameState():
    oppPreviousMoves = list()
    PreviousMoves = list()
    turnCount = 0
    opponentName = ""
    pointsToWin = 0
    maxRounds = 0
    dynamiteCount = 0
    oppDynamiteCount = 0


# Available moves
class Actions(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    DYNAMITE = 4
    WATERBOMB = 5

winning_pairs = {Actions.ROCK: [Actions.SCISSORS, Actions.WATERBOMB], Actions.PAPER: [Actions.ROCK, Actions.WATERBOMB],
                 Actions.SCISSORS: [Actions.PAPER, Actions.WATERBOMB], Actions.DYNAMITE: [Actions.ROCK, Actions.PAPER, Actions.SCISSORS],
                 Actions.WATERBOMB: [Actions.DYNAMITE]}

# dictionary mapping each action to the actions it loses against
losing_pairs = {Actions.ROCK: [Actions.DYNAMITE, Actions.PAPER], Actions.PAPER: [Actions.SCISSORS, Actions.DYNAMITE],
                Actions.SCISSORS: [Actions.ROCK, Actions.DYNAMITE], Actions.DYNAMITE: [Actions.WATERBOMB],
                Actions.WATERBOMB: [Actions.ROCK, Actions.PAPER, Actions.SCISSORS]}

class Move(Resource):
    game_state = None

    def __init__(self, **kwargs):
        self.game_state = kwargs['game_state']

    # Return bot's move for next round
    # Make changes here
    def get(self):
        # Increment turn count
        self.game_state.turnCount = self.game_state.turnCount + 1

        # Respond randomly
        return make_response(choosemove(), 200)

    # Recieving opponent's last move
    def post(self):
        # Parse data from post
        args = parser.parse_args()
        print('Opponent used: ' + args['lastOpponentMove'])

        # Store last move in the game state
        self.game_state.oppPreviousMoves.append(args['lastOpponentMove'])
        movereceived(args['lastOpponentMove'])


class Start(Resource):
    game_state = None

    def __init__(self, **kwargs):
        self.game_state = kwargs['game_state']

    # Start game
    def post(self):
        # Parse data from post
        args = parser.parse_args()

        # Set game state
        self.game_state.opponentName = args['opponentName']
        self.game_state.pointsToWin = args['pointsToWin']
        self.game_state.maxRounds = args['maxRounds']
        self.game_state.dynamiteCount = args['dynamiteCount']

        # Clear from previous game
        self.game_state.oppPreviousMoves = list()
        self.game_state.turnCount = 0

        print('###### Start Game #######')
        print('Opponent Name: ' + self.game_state.opponentName)
        print('Points to win: ' + str(self.game_state.pointsToWin))
        print('Max rounds: ' + str(self.game_state.maxRounds))
        print('Dynamite Count: ' + str(self.game_state.dynamiteCount))

        for key in opponent_decision_making:
            opponent_decision_making[key] = 0


def dynamiteratio():
    global state
    return state.oppDynamiteCount / (state.maxRounds - state.turnCount)

def movereceived(moveinp):
    global state
    if moveinp == "dynamite":
        state.oppDynamiteCount+=1

# compares the previous move of the opponent on turn x to;
# opponent's previous move
# our previous move
# identifies whether the opponent's algorithm is making decisions based on our/their past moves, NOT including repetition

def previous_moves_comparison():

    global state

    # checks the opponent's most recent move against both its and our previous moves, and increments the_opponent+decision_making dictionary appropriately
    if len(state.PreviousMoves) >= 1 and len(state.oppPreviousMoves) >= 2:
        opponents_last_move = state.oppPreviousMoves[-1]
        opponents_previous_move = state.oppPreviousMoves[-2]

        our_previous_move = state.PreviousMoves[-2]

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

    beat_opp_prev_ratio = opponent_decision_making["beat_opp_prev"]/len(state.oppPreviousMoves)
    if beat_opp_prev_ratio > 0.5:
        action = random.choice(losing_pairs[opponents_last_move])

        beat_our_prev_ratio = opponent_decision_making["beat_our_prev"]/len(state.oppPreviousMoves)
    if beat_our_prev_ratio > 0.5:
        action = random.choice(losing_pairs[our_previous_move])

        lose_opp_prev_ratio = opponent_decision_making["lose_opp_prev"]/len(state.oppPreviousMoves)
    if lose_opp_prev_ratio > 0.5:
        action = random.choice(winning_pairs[opponents_last_move])

    lose_our_prev_ratio = opponent_decision_making["lose_our_prev"]/len(state.oppPreviousMoves)
    if lose_our_prev_ratio > 0.5:
        action = random.choice(winning_pairs[our_previous_move])

    if action:
        return action.value
    else:
        return None

def choosemove():
    options=[]
    global state
    merryoption = previous_moves_comparison()
    dratio=dynamiteratio()
    if merryoption is not None:
        if not (merryoption==4 and dratio<0.01):
            options.append(merryoption)


    if len(options)==0:
        actiontotake=Actions(random.randint(1, 5)).name
        state.PreviousMoves.append(actiontotake)
        return actiontotake
    elif len(options)==1:
        actiontotake=Actions(options[0]).name
        state.PreviousMoves.append(actiontotake)
        return actiontotake
    elif len(options)>1:
        actiontotake = Actions(options[random.randint(0,len(options)-1)])
        state.PreviousMoves.append(actiontotake)
        return actiontotake
    else:
        print("Aaaaaa error this wasnt supposed to happen im sad")







move = None
# Init game state
state = GameState()

# Bind API resources
api.add_resource(Move, '/move', resource_class_kwargs={'game_state': state})
api.add_resource(Start, '/start', resource_class_kwargs={'game_state': state})

if __name__ == '__main__':
    # Listen externally on port 80
    bot.run(host='0.0.0.0', port=80)
