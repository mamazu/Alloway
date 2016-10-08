from abc import abstractmethod
# ClassOfDrawable
from tools.VecMath import Pane, Vec2D


class Drawable(Pane):
    def __init__(self, pos=None, size=None):
        Pane.__init__(self, pos, size)

    def set(self, pane):
        if isinstance(pane, Pane):
            self.pos = pane.pos
            self.size = pane.size
            return True
        else:
            return False

    def __mul__(self, other):
        Pane.__mul__(self, other)

    @abstractmethod
    def draw(self, surf):
        pass


class TextPane(Drawable):
    DEFAULTCOLOR = (0, 0, 0)
    DEFAULTFONTSIZE = 12

    ALIGN_LEFT = 1
    ALIGN_CENTER = 2
    ALIGN_RIGHT = 3

    VALIGN_TOP = -1
    VALIGN_CENTER = -2
    VALIGN_BOTTOM = -3

    def __init__(self, text, fontsize=None, color=None):
        Drawable.__init__(self)
        self.text = str(text)
        self.fs = fontsize if fontsize is not None else TextPane.DEFAULTFONTSIZE
        self.fc = color if color is not None else TextPane.DEFAULTCOLOR
        self.bg = None
        self.textRect = None
        self.align = (TextPane.ALIGN_LEFT, TextPane.VALIGN_CENTER)
        self.update()

    def setAlign(self, align=None, valign=None):
        align = align if align is not None else self.align[0]
        valign = valign if valign is not None else self.align[1]
        self.align = (align, valign)

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
