class Vec2D:
    def __init__(self, x=0, y=0, vec=None):
        """
        Constructor of the vector
        :param x: x value
        :type x: float
        :param y: y value
        :type y: float
        """
        self.x = x
        self.y = y
        if vec is None:
            return
        if Vec2D.isVec(vec):
            self.x = vec.x
            self.y = vec.y
        elif len(vec) == 2:
            self.x = vec[0]
            self.y = vec[1]

    def __add__(self, other):
        """
        Adds two vectors componentwise and adds a scale and a vector
        :param other: Second part of the sum
        :type other: int, float, Vec2D
        :return: Returns the sum
        :rtype: Vec2D
        """
        if isinstance(other, Vec2D):
            return Vec2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vec2D(self.x + other, self.y + other)

    def __sub__(self, other):
        """
        Subtracts a vector by.
        :param other: Other must have specified a __neg__ method
        :type other: int, float, Vec2D
        :rtype: Vec2D
        """
        return self + (-other)

    def __neg__(self):
        """
        Returns the negative value of the vector
        :rtype: Vec2D
        """
        return Vec2D(-self.x, -self.y)

    def __mul__(self, other):
        """
        Multiplies an int with a vector with a number or a vector.
        If the parameter other is a number it, scalar multiplication will be applied.
        If the parameter is a vector the componetns will be multiplied one by one.
        :type other: int, float, Vec2D
        :rtype: Vec2D
        """
        if Vec2D.isVec(other):
            return Vec2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vec2D(self.x * other, self.y * other)

    def __div__(self, other):
        """
        Returns the division
        :type other: float
        :return: Vector
        :rtype: Vec2D
        """
        if other == 0:
            return None
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self.x / other, self.y / other)

    def __eq__(self, other):
        """
        Checks if two vectors are equal
        :param other:
        :type other: Vec2D
        :return:
            True if equal, false otherwise
        :rtype: bool
        """
        if not Vec2D.isVec(other):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        Checks if two vectors are unequal
        :param other:
        :type other: Vec2D
        :return:
            False if equal, true otherwise
        :rtype: bool
        """
        return not (self == other)

    def __lt__(self, other):
        if Vec2D.isVec(other):
            return self.x < other.x and self.y < other.y
        if isinstance(other, int) or isinstance(other, float):
            return self.x < other and self.y < other

    def __gt__(self, other):
        if Vec2D.isVec(other):
            return self.x > other.x and self.y > other.y
        if isinstance(other, int) or isinstance(other, float):
            return self.x > other and self.y > other

    def __len__(self):
        return 2

    def getTuple(self):
        """
        Returns the tuple of the vector
        :rtype: tuple
        """
        intversion = self.getInt()
        return intversion.x, intversion.y

    def getInt(self):
        """
        Returns the integer version of the vector.
        :rtype: Vec2D
        """
        if Vec2D.isVec(self.x) or Vec2D.isVec(self.y):
            print(self)
            return Vec2D(0, 0)
        return Vec2D(int(self.x), int(self.y))

    def getLength(self):
        import math
        return math.sqrt(self.x**2 + self.y**2)

    def set(self, value):
        """
        Sets the value of the vector based on a tuple
        :param value:
        :type value: tuple or Vec2D
        :return: The new vector
        :rtype: Vec2D
        """
        if len(value) == 2:
            self.x, self.y = value
        elif Vec2D.isVec(value):
            self.x = value.x
            self.y = value.y
        else:
            self.x, self.y = (0, 0)
        return self

    @staticmethod
    def isVec(vec):
        """
        Checks if the parameter is a vector
        :param vec:
        :type vec: Vec2D
        :return: True if it is a vector, false otherwise
        :rtype: bool
        """
        return isinstance(vec, Vec2D) and vec is not None

    def __str__(self):
        """
        Returns the string representation of the vector
        :rtype: str
        """
        return "Vec2(%s|%s)" % (self.x, self.y)

    def __repr__(self):
        """
        Returns the string representation of the vector
        :rtype: str
        """
        return str(self)

class Pane:
    from pygame import Rect
    def __init__(self, pos=None, size=None):
        """
        Constructor of the pane object
        :param pos: Position of the pane
        :type pos: Vec2D
        :param size: Size of the pane
        :type size: Vec2D
        """
        self.pos = pos if Vec2D.isVec(pos) else Vec2D(0, 0)
        self.size = size if Vec2D.isVec(size) else Vec2D(0, 0)

    def set(self, value):
        """
        Sets the values of a pane based on a rectangle
        :param value:
        :type value: pygame.Rect
        :return: Returns the pane
        :rtype: Pane
        """
        if isinstance(value, Rect):
            self.pos = Vec2D(value.left, value.top)
            self.size = Vec2D(value.width, value.height)
        return self

    def getRect(self):
        """
        Gets the rectangle object based on the pane
        :return:
        :rtype: pygame.Rect
        """
        from pygame import Rect
        pos = self.pos.getInt()
        size = self.size.getInt()
        return Rect(pos.x, pos.y, size.x, size.y)

    def __add__(self, other):
        """
        Adds two panes together if the other one is not a pane or a tuple the
        :param other: Pane to be added
        :type other: tuple or Pane
        :return: The new pane
        :
        """
        result = Pane()
        if len(other) == 4:
            result.pos = self.pos + Vec2D(other[0], other[1])
            result.size = self.size + Vec2D(other[2], other[3])
        elif isinstance(other, Pane):
            result.pos = self.pos + other.pos
            result.size = self.size + other.size
        return result

    def __mul__(self, other):
        """
        Multiplies the size of the pane by a factor
        :param other: factor
        :type other: int or float
        :return: The new pane
        :rtype: Pane
        """
        if isinstance(other, int) or isinstance(other, float):
            return self.size * other

    def __str__(self):
        """
        Returns the string version of the pane
        :return:
        :rtype: str
        """
        return "Pos: %s; Size: %s" % (self.pos, self.size)

    def __iadd__(self, other):
        return other
