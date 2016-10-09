from tools.utils import Drawable
from tools.VecMath import Vec2D

class TextPane(Drawable):
    DEFAULTCOLOR = (0, 0, 0)
    DEFAULTFONTSIZE = 12

    def __init__(self, text, fontsize=None, color=None):
        Drawable.__init__(self)
        self.text = str(text)
        self.fs = fontsize if fontsize is not None else TextPane.DEFAULTFONTSIZE
        self.fc = color if color is not None else TextPane.DEFAULTCOLOR
        self.bg = None
        self.textRect = None
        self.update()

    def setText(self, text):
        self.text = str(text)
        self.update()

    def setBGcolor(self, color=None):
        if color is None or len(color) == 3:
            self.bg = color
        else:
            self.bg = None

    def update(self):
        from pygame.font import Font
        self.textRect = Font(None, self.fs).render(self.text, 1, self.fc)
        rect = self.textRect.get_rect()
        self.size = Vec2D(rect.width, rect.height)

    def draw(self, surf):
        if self.bg is not None:
            from pygame.draw import rect
            rect(surf, self.bg, self.getRect())
        surf.blit(self.textRect, self.pos.getTuple())

class MultilineText(Drawable):
    def __init__(self, text, fontsize=None, color=None):
        self.lines = [TextPane(line) for line in text.split('\n')]

    def draw(self, surf):
        textVec = self.pos
        for i, line in enumerate(self.lines):
            line.pos = textVec
            line.draw(surf)
            textVec += Vec2D(0, line.size.y)
