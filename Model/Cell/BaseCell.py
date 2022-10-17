class Cell:
    _x: int = 0  # 2D vector --> position
    _y: int = 0

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def click(self):
        self._isDiscovered = True
        return self.__isMine

    def asExplode(self):
        return self.__isMine & self._isDiscovered

    def getNbMineClose(self):
        if (not self.__isMine) & self._isDiscovered: return self.__nbMineClose

    def getValue(self):
        if self.asExplode():
            return "Mine"
        elif not self._isDiscovered:
            return "Unknown"
        else:
            return str(self.__nbMineClose)