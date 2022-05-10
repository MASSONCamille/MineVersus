
class Cell:
    _x: int = 0   # 2D vector --> position
    _y: int = 0

    __isMine: bool = False
    _isDiscovered: bool = False

    __nbMineClose: int = 0 # no mandatory but usefull to dont waste time in algorithm

    def __init__(self, x: int, y: int, isMine: bool, nbMineClose: int):
        self._x = x
        self._y = y
        self.__isMine = isMine
        self.__nbMineClose = nbMineClose
        self._isDiscovered = False

    def click(self):
        self._isDiscovered = True
        return self.__isMine

    def asExplode(self):
        return self.__isMine & self._isDiscovered

    def getNbMineClose(self):
        if (not self.__isMine) & self._isDiscovered: return self.__nbMineClose

    def getValue(self):
        if self.asExplode():            return "Mine"
        elif not self._isDiscovered:    return "Unknown"
        else:                           return str(self.__nbMineClose)