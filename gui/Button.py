from tools.utils import TextPane
from tools.VecMath import Vec2D

class Button(TextPane):
    # TODO: add parameters to function call
    def __init__(self, text, action=None):
        TextPane.__init__(self, text)
        if(callable(action)):
            self.action = action
        else:
            self.action = None

    def click(self, mousePos=Vec2D(0, 0)):
        relPos = Vec2D(0, 0, mousePos) - self.pos
        if(relPos > 0 and relPos < self.size):
            if(self.action is not None):
                self.action()
            return True
        else:
            return False
