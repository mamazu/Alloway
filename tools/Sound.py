from gui.Button import Button
from pygame import mixer as mix

class Sound(Button):
    DEFAULTSOUNDS = {
        "player": "res/Sounds/playerBall.wav",
        "wall": "res/Sounds/wallBall.wav",
        "block": "res/Sounds/blockBall.wav",
        "gameOver": "res/Sounds/gameOver.wav"
    }

    # Constructor
    def __init__(self, on=False):
        Button.__init__(self, "Sound", self.toggleSound)
        mix.init()
        self.sounds = {}
        self.load(Sound.DEFAULTSOUNDS)
        self.fc = (255, 0, 0) if on else (0, 0, 0)
        #Printing debug
        print("Sound created and %i sounds loaded" % len(self.sounds))

    def load(self, moreSounds={}):
        from os.path import isfile
        for key, fileName in moreSounds.items():
            if not isfile(fileName):
                print("Could not load file %s" % fileName)
                continue
            self.sounds[key] = mix.Sound(fileName)

    # Toggles the sound
    def toggleSound(self):
        # toggles the color from red to black
        self.fc = (0, 0, 0) if self.fc == (255, 0, 0) else (255, 0, 0)
        self.setSize()

    # Plays the sound
    def play(self, what="player"):
        if not self.isOn:
            return None
        # Tries to play the sound of the sound array
        try:
            self.sounds[what].play()
        except KeyError:
            print("Could not find sound")
