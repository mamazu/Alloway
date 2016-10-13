from abc import abstractmethod
# ClassOfDrawable
from tools.VecMath import Pane


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
        raise NotImplementedError('You have not implemented draw yet')
