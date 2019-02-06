import itertools, random

class Markov:
    def __init__(self):
        self.len = 7
        self.combinations = {i:0 for i in list(itertools.product("12345",repeat=self.len))}
        self.recentMoves = []
    def mainMarkov(self):
        possibleMoves = [i for i in self.combinations.keys() if tuple(self.recentMoves) == i[:-1]]
        newMoves = {i:self.combinations[i] for i in possibleMoves}
        try:
            print(newMoves.get)
            finish = max(newMoves, key = newMoves.get)[-1]
        except ValueError:
            if len(set(newMoves.values())) == len(newMoves.values()):
                finish = str(random.randint(1,5))
            else:
                g = min(newMoves, key = newMoves.get[-1])
                finish = str(random.choice(list("12345".replace(g,""))))
        y = "12345"[("12345".index(finish)+1)%6]
        if (y == 1):
            return random.choice(losing_pairs[Actions.ROCK]).value
        elif (y == 2):
            return random.choice(losing_pairs[Actions.PAPER]).value
        elif (y == 3):
            return random.choice(losing_pairs[Actions.SCISSORS]).value
        elif (y == 4):
            return random.choice(losing_pairs[Actions.DYNAMITE]).value
        else:
            return random.choice(losing_pairs[Actions.WATERBOMB]).value


    def run(self,move):
        if len(self.recentMoves) < self.len:
            self.recentMoves.append(move)
        else:
            self.recentMoves.pop(0)
            self.recentMoves.append(move)

x = Markov()
## every time we get a number
x.run(NUMBERGOESHERE)

print(x.mainMarkov())
## returns what we think they will give next

