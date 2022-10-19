
class Cell:
    _id: int = None

    __isMine: bool = False
    _isDiscovered: bool = False

    # no mandatory but usefull to dont waste time in algorithm
    _closeCells: list[list[int]] = []
    _nbMineClose: int = None

    def __init__(self, id: int, isMine: bool):
        self._id = id
        self.__isMine = isMine
        self._isDiscovered = False

    def click(self):
        self._isDiscovered = True
        return self.__isMine

    def asExplode(self):
        return self.__isMine & self._isDiscovered

    def getValue(self):
        if not self._isDiscovered:  return 10                       # 10 = unknow
        elif self.__isMine:          return 9                       # 9 = mine
        else:                       return self._nbMineClose   # [0;8] = how many mine around