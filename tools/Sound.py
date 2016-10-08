from gui.Button import Button
from pygame import mixer as mix
import threading

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
        self.isOn = bool(on)
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
        self.isOn = not self.isOn
        self.fc = (255, 0, 0) if self.isOn else (0, 0, 0)
        self.update()

    # Plays the sound
    def play(self, what="player"):
        if not self.isOn:
            return None
        # Tries to play the sound of the sound array
        try:
            self.sounds[what].play()
        except KeyError:
            print("Could not find sound")
