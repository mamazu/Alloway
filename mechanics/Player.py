from tools.VecMath import Vec2D
from tools.utils import Drawable


class Player(Drawable):
    PLAYERSPEED = 10
    PLAYERSIZE = Vec2D(150, 10)

    # Constructor
    def __init__(self, size=None):
        if Vec2D.isVec(size):
            Drawable.__init__(self,None, size)
        else:
            Drawable.__init__(self,None, Player.PLAYERSIZE)
        self.offsetY = 30
        self.speed = 5
        self.sizeScale = 1
        self.movement = Vec2D(0, 0)
        print("Player created")

    # Resizing the player
    def setSize(self, scale):
        if isinstance(scale, float) or isinstance(scale, int):
            self.size = Player.PLAYERSIZE*scale
        else:
            self.size = Player.PLAYERSIZE

    # Setting speed
    def setSpeed(self, x):
        self.speed = Player.PLAYERSPEED * x

    # Moving the player+checking for collisions
    def move(self):
        self.pos += self.movement * self.speed
        # self.pos.x = max(0, self.pos.x)
        # self.pos.x = min(sSize[0] - self.size.x, self.pos.x)

    # Checks if the Player is hitting the Ball
    def collide(self, ball):
        if self.collisionDetection(ball):
            # Collision rate
            center = self.pos.x + self.size.x / 2
            speed = abs(Ball.movement[0]) + abs(Ball.movement[1])
            rate = (Ball.pos[0] - center) / (self.size.x / 2) * speed
            ball.movement = Vec2D(rate, -abs(speed - abs(rate)))
            ball.pos = (ball.pos[0], sSize[1] - (self.size.y + self.offsetY + Ball.size + 1))
            print(ball.movement)
            Sound.playSound()

    # Detects whether the Ball has hit the player
    def collisionDetection(self, ball):
        ballRect = ball.getRect()
        return self.getRect().collide(ballRect)

    # Puting the player out on the screen
    def draw(self, screen):
        from pygame.draw import rect
        rect(screen, (0, 0, 0), self.getRect())
