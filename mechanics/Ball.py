from tools.VecMath import Vec2D
from tools.utils import Drawable
from gui.Text import TextPane

# BallClass
class Ball(Drawable):
    DEFAULTSIZE = 80
    FAIL = 0
    BOUNCE = 1
    NONE = 2

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

    # Setting the speed of the ball
    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    # Get the relative position of an object
    def relPos(self, obj):
        if not isinstance(obj, Drawable):
            return self.pos - obj.pos + (obj.size / 2)
        return None

    # Moves the ball acording to his movement
    def move(self):
        self.pos += self.movement * self.speed

    # Starting ball movement
    def moveRand(self):
        if self.movement != Vec2D(0, 0):
            return False
        from random import randint
        self.movement = Vec2D(randint(-1, 4), -4)
        while self.movement.x == 0:
            self.movement.x = randint(-1, 4)
        print("Starting Speed: %s" % self.movement)
        return True

    def collides(self, other):
        if isinstance(other, Drawable):
            if self.getRect().colliderect(other.getRect()):
                self.bounceY()
                return True
            return False
        else:
            return None

    # Changes the moving direction of the ball
    def bounceX(self): self.movement.x = -self.movement.x
    def bounceY(self): self.movement.y = -self.movement.y

    # Checks if the ball collides with something
    def constrain(self, boundery):
        # Top
        if self.pos.y < 0:
            self.bounceY()
            self.pos = Vec2D(self.pos.x, 0)
            return Ball.BOUNCE
        # Right
        elif (self.pos + self.size).x >= boundery.x:
            self.bounceX()
            self.pos = Vec2D(boundery.x - (self.size.x + 1), self.pos.y)
            return Ball.BOUNCE
        # Left
        elif self.pos.x < 0:
            self.bounceX()
            self.pos = Vec2D(0, self.pos.y)
            return Ball.BOUNCE
        #Down
        elif (self.pos + self.size).y > boundery.y:
            return Ball.FAIL
        return Ball.NONE

    # Draws the ball on the screen
    def draw(self, screen):
        from pygame.draw import circle
        circle(screen, (255, 0, 0), (self.pos + self.size / 2).getTuple(), self.size.y / 2)
