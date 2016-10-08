from tools.utils import Drawable
import os

TEXTUES = []
FILETYPESFORTEXTURES = ["jpg", "png", "gif", "bmp", "pcx", "tga", "tif", "lbm", "pbm", "pgm", "ppm", "xpm"]
for root, dirs, files in os.walk("Images"):
    for file in files:
        if file[-3:].lower() in FILETYPESFORTEXTURES:
            TEXTUES.append(os.path.join("Images", file))


# BlockClass
class Block(Drawable):
    BLOCKSIZE = (50, 25)

    # Constructor
    def __init__(self, position, size=1):
        import random, pygame
        from tools.utils import Vec2D
        self.imageOverLay = None
        #self.effekt = ClassOfEffect("none")
        self.pos = Vec2D(0, 0, position)
        self.size = Vec2D(size * Block.BLOCKSIZE[0], Block.BLOCKSIZE[1])
        if len(TEXTUES) != 0:
            image = pygame.image.load(random.choice(TEXTUES))
            image = pygame.transform.scale(image, self.expansions)
            self.imageOverLay = image
        else:
            self.imageOverLay = None

    # Drawing the block
    def draw(self, screen):
        from pygame.draw import rect
        if self.imageOverLay is not None:
            screen.blit(self.imageOverLay, self.pos.getTuple())
        else:
            rect(screen, (255, 0, 0), self.getRect())
        rect(screen, (0, 0, 0), self.getRect(), 2)

    # Collision with coordinates
    def collides(self, ball):
        if isinstance(ball, Drawable):
            ballRect = ball.getRect()
            return self.getRect().collide(ballRect)
        return None

    # Returns the name of the effect
    def getEffect(self, what="type"):
        if what == "type":
            return self.effekt.typeName
        elif what == "object":
            return self.effekt
        else:
            return False

    # Returns whether the Block has an effect
    def hasEffect(self):
        return self.effekt.typeName != "none"


# Levelclass
class Level(Drawable):
    # Constructor
    def __init__(self):
        from tools.utils import TextPane
        self.levelid = 1
        self.time = 30
        self.blocks = []
        self.text = TextPane("", 19)
        self.switchLevel(1)
        print("Level created")

    # Changes the level to a certain id
    def switchLevel(self, newLevel):
        self.levelid = newLevel
        self.setPattern()
        self.text.setText("Level: " + str(self.levelid))
        print("Level %s" % self.levelid)

    # Draws the level id on the screen
    def draw(self, screen):
        self.text.draw(screen)
        for block in self.blocks:
            block.draw(screen)

    # Sets the Block pattern for the level
    def setPattern(self):
        if self.levelid == 1:
            pattern = (
                ((10, 10), 1), ((10 + Block.BLOCKSIZE[0], 10), 1), ((10 + Block.BLOCKSIZE[0] * 2, 10), 2),
                ((10, 10 + Block.BLOCKSIZE[1]), 2), ((10 + Block.BLOCKSIZE[0] * 2, 10 + Block.BLOCKSIZE[1]), 2),
                ((10, 10 + Block.BLOCKSIZE[1] * 2), 3), ((10 + Block.BLOCKSIZE[0] * 3, 10 + Block.BLOCKSIZE[1] * 2), 1),
                ((10, 10 + Block.BLOCKSIZE[1] * 3), 4),
                ((10 + int(Block.BLOCKSIZE[0] * 3.5), 10 + int(Block.BLOCKSIZE[1] * 4)), 2)
            )
            self.time = 30
            # Player.setSpeed(1.5)
        elif self.levelid == 2:
            pattern = (
                ((10, 20), 1),
                ((10, 40), 1)
            )
            self.time = 30
            # Setting new player size
            # Player.setSize(0.8)
            # Ball.setSpeed(1.325)
        else:
            pattern = ()
            self.time = 100
            # Player.setSpeed(0.1)
        for everyBlock in pattern:
            self.blocks.append(Block(everyBlock[0], everyBlock[1]))

    def collide(self, ball):
        hasCollided = []
        for block in self.blocks:
            hasCollided.append(block.collides(ball))
        print(hasCollided)
        self.blocks = [block for i, block in enumerate(self.blocks) if not hasCollided[i]]
        ball.bounce()
        return any(hasCollided)

    # Returns the ticktime of the level
    def getTime(self):
        return self.time
