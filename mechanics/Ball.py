from tools.VecMath import Vec2D
from tools.utils import Drawable, TextPane


class MovementMode(TextPane):
    # Property
    DEFAULTMODE = 0
    MODES = ["Bowling", "Bouncing", "Ghost"]

    # Constructor
    def __init__(self, mode=None):
        if mode is None or not isinstance(mode, int):
            self.mode = 0
        else:
            self.mode = mode % len(self.mode)
        TextPane.__init__(self, self, 18)
        print("Mode: %i" % self.mode)

    # Toggles the mode
    def toggle(self):
        self.mode = (self.mode + 1) % len(MovementMode.MODES)
        self.setText(self)

    def __int__(self):
        return self.mode

    def __str__(self):
        return MovementMode.MODES[self.mode]


# BallClass
class Ball(Drawable):
    DEFAULTSIZE = 80

    # Constructor
    def __init__(self, size=None):
        if isinstance(size, int) or isinstance(size, float):
            Drawable.__init__(self, pos=Vec2D(0, 0), size=Vec2D(size, size))
        else:
            Drawable.__init__(self, pos=Vec2D(0, 0), size=Vec2D(Ball.DEFAULTSIZE, Ball.DEFAULTSIZE))
        self.movement = Vec2D(0, 0)
        self.speed = 1
        print("Ball created")

    # Sets the new position of the Ball
    def setPosition(self, position):
        self.pos if Vec2D.isVec(position) else Vec2D(0, 0)

    # Get the relative position of an object
    def relPos(self, OBJpos):
        erg = ''
        if self.pos.x > OBJpos.pos.x:
            erg += 'R'
        else:
            erg += 'L'
        if self.pos.y > OBJpos.pos.y:
            erg += 'U'
        else:
            erg += 'O'
        return erg

    # Moves the ball acording to his movement
    def move(self):
        if self.movement != Vec2D(0, 0):
            self.pos += self.movement * self.speed
            self.collides()
            Player.collidePlayer()
            # Checking the Blocks
        if round(self.movement.y) == 0 and self.movement.x != 0:
            self.movement.y = -1
        if self.pos.y < 0:
            self.pos = Vec2D(self.pos.x, self.size)
        if self.pos.x < 0:
            self.pos = Vec2D(self.size, self.pos.x)

    # Starting ball movement
    def moveRand(self):
        if self.movement == Vec2D(0, 0):
            from random import randint
            self.movement = Vec2D(randint(-1, 4), -4)
            print("Starting Speed: %s" % self.movement)
        else: print("Current Speed: %s" % self.movement)

    # Changes the moving direction of the ball
    def bounce(self, direction):
        if self.mode == "Bouncing":
            self.movement.y = -self.movement.y
            return True
        from random import randint
        if direction in (0, 2):
            # print("Bounce of the top or player")
            if self.pos.x <= self.size:
                Sound.playSound("wall")
                return True
            self.movement = Vec2D(self.movement.x - randint(0, 1), -self.movement.y)
        elif direction in (1, 3):
            self.movement.x = -self.movement.x - randint(0, 1)
            return True
            # print("Bounce of one side")
        else:
            print("Bouncing direction not defined")

    # Checks if the ball collides with something
    def collides(self):
        # Top
        if self.pos.y < self.size:
            self.bounce(0)
            self.pos = Vec2D(self.pos.x, self.size + 1)
        # Right
        elif self.pos.x + self.size.x > sSize[0]:
            self.bounce(1)
            self.pos = Vec2D(sSize[0] - (self.size + 1), self.pos.y)
        # Down
        elif self.pos.y >= sSize[1] - self.size:
            print("Game Over")
            gameOver()
        # Left
        elif self.pos.x < self.size:
            self.bounce(3)
            self.pos = Vec2D(self.size + 1, self.pos.y)

    # Setting the speed of the ball
    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    # Draws the ball on the screen
    def draw(self, screen):
        from pygame.draw import circle
        circle(screen, (255, 0, 0), (self.pos + self.size / 2).getTuple(), self.size.y / 2)
