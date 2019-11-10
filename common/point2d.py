
class Point2d(object):
    def __init__(self, x, y, cost=float('inf')):
        self.__x = x
        self.__y = y
        self.__have_parent = False
        self.__cost = cost

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def location(self):
        return (self.__x, self.__y)

    def set_cost(self, cost):
        self.__cost = cost

    def cost(self):
        return self.__cost

    def set_parent(self, parent):
        self.__parent = parent
        self.__have_parent = True

    def parent(self):
        return self.__parent

    def have_parent(self):
        return self.__have_parent

    def __cmp__(self, other):
        return self.x() != other.x() or self.y() != other.y()

    def __hash__(self):
        return hash((self.__x, self.__y))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.x() == other.x() and self.y() == other.y()
