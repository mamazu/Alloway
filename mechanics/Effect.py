import random


class Effect:
    active = True
    typeName = "none"
    duration = 0
    tickTime = 0

    # Constructor
    def __init__(self, name, duration=20):
        self.typeName = name
        self.setDuration(duration)
        # Doing the effect
        if self.typeName == "BallSlower":           ball.setSpeed(0.5)
        elif self.typeName == "PlayerSlower":       player.setSpeed(0.7)
        elif self.typeName == "PlayerBooster":      player.setSpeed(1.5)
        elif self.typeName == "BallBooster":        ball.setSpeed(1.3)

    # Sets the duration of an effect
    def setDuration(self, newDuration):
        try:
            newDuration = int(newDuration)
        except Exception as e:
            print(e)
            return False
        else:
            self.duration = newDuration
            return True

    # Returns the duration of the effect
    def getDuration(self):
        return self.duration

    # Ticks the effect (removes one from duration)
    def tick(self):
        self.tickTime -= 1
        if self.tickTime < 0:
            self.duration -= 1
            self.tickTime = level.getTime()
        if self.duration == 0:
            # Undoing the effect
            if self.typeName.find("Player") == 0:
                player.setSpeed(1)
                Effect.remove(self)
            elif self.typeName.find("Ball") == 0:
                ball.setSpeed(1)
                Effect.remove(self)

    # Draws the effect duration on the screen
    def drawEffect(self, displayID):
        text = renderText(self.typeName + ": " + str(self.getDuration()), 20, (255, 255, 0))
        rect = text.get_rect()
        vz = -1 if (displayID % 2) else 1
        screen.blit(text, (sSize[0] - rect.width, int((sSize[1] + (rect.height + 5) * displayID * vz) // 2)))

    @staticmethod
    def getRandEffekt():
        allEffekts = ['BallSlower', 'PlayerSlower', 'BallBooster', 'PlayerBooster']
        return random.choice(allEffekts)