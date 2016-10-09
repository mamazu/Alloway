class Highscore:
    def __init__(self):
        self.playerName = 'Please enter your name!'
        self.blocked = True

    # Saves the score to a file
    @staticmethod
    def saveToFile(name, score, level):
        import datetime, os
        curDate = datetime.datetime.now().strftime('%d %b %Y')
        if os.path.isdir('Scores'):
            Scorefile = open('Scores/' + curDate + '.txt', 'a')
        else:
            os.makedirs('Scores')
            Scorefile = open('Scores/' + curDate + '.txt', 'w')
        Scorefile.write(name + ' just scored ' + str(score) + ' points in level ' + str(level) + '.\n')
        Scorefile.close()


# PointsClass
from gui.Text import TextPane

class Score(TextPane):
    DEFAULTSCORE = 0

    # Constructor
    def __init__(self, startVal=None):
        if isinstance(startVal, int):
            self.score = startVal
        else:
            self.score = Score.DEFAULTSCORE
        TextPane.__init__(self, self.score, 30)

    # Adding points to the score
    def __add__(self, addVal):
        score = Score(self.score + addVal)
        score.pos = self.pos + self.size - score.size
        return score

    # Subtract points
    def __sub__(self, subVal):
        score = Score(self.score - addVal)
        score.pos = self.pos + self.size - score.size
        return score

    # Resetting the score to 0
    def reset(self):
        self.score = Score.DEFAULTSCORE
