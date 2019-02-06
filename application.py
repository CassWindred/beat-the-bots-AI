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


def getstate():
    global state
    return state

def dynamiteratio():
    global state
    return state.oppDynamiteCount / (state.maxRounds - state.turnCount)

def movereceived(move):
    global state
    if move == "dynamite":
        state.oppDynamiteCount+=1

def choosemove():
    options=[]
    global state
    merryoption = merryfunction()
    dratio=dynamiteratio()
    if merryoption is not None:
        if not (merryoption==4 and dratio<0.01):
            options.append(merryoption)


    if len(options)==0:
        return Actions(random.randint(1, 5)).name
    elif len(options)==1:
        return Actions(options[0]).name
    elif len(options)>1:
        return Actions(options[random.randint(0,len(options)-1)])
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
