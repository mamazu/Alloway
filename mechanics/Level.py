from tools.utils import Drawable
from tools.Debug import Debug
import os

TEXTUES = []
FILETYPESFORTEXTURES = ["jpg", "png", "gif", "bmp", "pcx", "tga", "tif", "lbm", "pbm", "pgm", "ppm", "xpm"]
for root, dirs, files in os.walk("res/Images"):
    for file in files:
        TEXTUES.append(os.path.join("res/Images", file))
#print(TEXTUES)

# BlockClass
class Block(Drawable):
    BLOCKSIZE = (50, 25)

    # Constructor
    def __init__(self, position, size):
        import random, pygame
        from tools.VecMath import Vec2D
        self.imageOverLay = None
        #self.effekt = ClassOfEffect("none")
        self.pos = Vec2D(0, 0, position)
        self.size = Vec2D(0, 0, size)
        if len(TEXTUES) != 0:
            image = pygame.image.load(random.choice(TEXTUES))
            #image = pygame.transform.scale(image, self.size.getTuple())
            self.imageOverLay = image
        else:
            self.imageOverLay = None

    # Drawing the block
    def draw(self, screen):
        from pygame.draw import rect
        if self.imageOverLay is not None:
            screen.blit(self.imageOverLay, self.pos.getTuple(), (0, 0, self.size.x, self.size.y))
        else:
            rect(screen, (255, 0, 0), self.getRect())
        rect(screen, (0, 0, 0), self.getRect(), 2)

    # Collision with coordinates
    def collides(self, ball):
        if isinstance(ball, Drawable):
            ballRect = ball.getRect()
            return self.getRect().colliderect(ballRect)
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
        Drawable.__init__(self)
        from gui.Text import TextPane
        self.levelid = 1
        self.time = 30
        self.blocks = []
        self.text = TextPane("", 19)
        self.switchLevel(1)
        Debug.printMessage("Level created")

    # Changes the level to a certain id
    def switchLevel(self, newLevel):
        self.levelid = newLevel
        self.setPattern()
        self.text.setText("Level: " + str(self.levelid))
        Debug.printMessage("Level %s" % self.levelid)

    # Draws the level id on the screen
    def draw(self, screen):
        self.text.draw(screen)
        for block in self.blocks:
            block.draw(screen)

    def load(self, levelname):
        import os, re
        filename = 'res/level/'+levelname
        if not os.path.isfile(filename):
            return []
        levelcontent = open(filename).read()
        blocks = []
        for line in levelcontent.split('\n'):
            if len(line) == 0: continue
            match = re.findall(r'(\d+)\s*[,;]\s*(\d+)\s*[,;]\s*(\d+)\s*[,;]\s*(\d+)\s*', line)
            blockdata = [int(blockProperty) for blockProperty in match[0]]
            block = Block(blockdata[:2], blockdata[2:])
            blocks.append(block)
        return blocks

    # Sets the Block pattern for the level
    def setPattern(self):
        if self.levelid == 1:
            self.blocks = self.load('level1hardcoded.lvl')
            self.time = 30
            # Player.setSpeed(1.5)
        elif self.levelid == 2:
            self.blocks = self.load('level2hardcoded.lvl')
            self.time = 30
            # Setting new player size
            # Player.setSize(0.8)
            # Ball.setSpeed(1.325)
        else:
            self.time = 100
            # Player.setSpeed(0.1)

    def levelCheck(self):
        if len(self.blocks) == 0:
            self.switchLevel(self.levelid + 1)
        return len(self.blocks)

    def setOffset(self, offset=None):
        from tools.VecMath import Vec2D
        if not Vec2D.isVec(offset) or offset is None:
            return
        for block in self.blocks:
            block.pos += offset

    def collides(self, obj):
        if not isinstance(obj, Drawable):
            return None
        hasCollided = []
        for block in self.blocks:
            hasCollided.append(block.collides(obj))
        self.blocks = [block for i, block in enumerate(self.blocks) if not hasCollided[i]]
        return any(hasCollided)

    # Returns the ticktime of the level
    def getTime(self):
        return self.time
