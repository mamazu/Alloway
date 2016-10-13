from tools.VecMath import Vec2D
from tools.utils import Drawable


class Player(Drawable):
    PLAYERSPEED = 10
    PLAYERSIZE = Vec2D(150, 10)

    # Constructor
    def __init__(self, size=None):
        from tools.Debug import Debug
        if Vec2D.isVec(size):
            Drawable.__init__(self,None, size)
        else:
            Drawable.__init__(self,None, Player.PLAYERSIZE)
        self.offsetY = 30
        self.speed = 5
        self.sizeScale = 1
        self.movement = Vec2D(0, 0)
        Debug.printMessage("Player created")

    # Resizing the player
    def setSize(self, scale):
        if Vec2D.isVec(scale):
            scale = scale.getLength()
        if isinstance(scale, float) or isinstance(scale, int):
            self.size = Player.PLAYERSIZE*scale
        else:
            self.size = Player.PLAYERSIZE

    # Setting speed
    def setSpeed(self, x):
        self.speed = Player.PLAYERSPEED * x

    # Moving the player+checking for collisions
    def move(self, screenWidth):
        self.pos += self.movement * self.speed
        self.pos.x = max(0, self.pos.x)
        self.pos.x = min(screenWidth - self.size.x, self.pos.x)

    # Puting the player out on the screen
    def draw(self, screen):
        from pygame.draw import rect
        rect(screen, (0, 0, 0), self.getRect())
