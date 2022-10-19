import copy
import random
from Model.Cell import *

class Grid:

#---| Variables & init |------------------------------------------------------------------------------------------------

    _height: int = 0
    _width: int = 0

    _nbMineTotal: int = 0
    _nbMineDiscover: int = 0

    __cellList: list[list[Cell]] = []   # register with a list of list:
                                        # list of line
                                        # line = list of Cases
    __lstMine: list[int] = []

    def __init__(self, height: int, width: int, nbMine: int):
        self._height = height
        self._width = width
        self._nbMineTotal = nbMine
        self.gererateGrid()


    def getCellFromCord(self, x, y):
        return self.__cellList[x][y]

    def getCellFromId(self, id):
        cell = self.__cellList[id // self._width][id % self._width]
        assert cell._id == id
        return cell

#---| Play functions |--------------------------------------------------------------------------------------------------

    def play(self, x, y):   # XY --> coord, x(0:h-1), y(0:w-1)
        return self.__cellList[x][y].click()   # x = line (h) | y = cell (w)
        # return True if cell has exploded

    def getPlayingGrid(self):  # return __cellList but with None for unknown cell
        listline = []
        for line in self.__cellList:
            lstcell = []
            for cell in line:
                lstcell.append(cell.getValue())
            listline.append(lstcell)
        return listline

    def getEndingGrid(self):  # return list[list[ list[discovered , cellVal] ]]
        listline = []
        for line in self.__cellList:
            lstcell = []
            for cell in line:
                cellDetail = [True, None]
                if not cell._isDiscovered:
                    cellDetail[0] = False
                    cell.click()    # for know the value
                cellDetail[1] = cell.getValue()
                lstcell.append(cellDetail)
            listline.append(lstcell)
        return listline


#---| Grid generation functions |---------------------------------------------------------------------------------------

    def gererateGrid(self):
        self.__cellList = []

        nbCase = self._width * self._height
        self.__lstMine = random.sample( list(range(0, nbCase)), self._nbMineTotal )  # generate a list with _nbMineTotal
                                                                                    # position
        for i in range(0, self._height):
            line = []
            for j in range(0, self._width):
                index = j + i * self._width
                cell = Cell(index, bool(index in self.__lstMine))
                self.__setCloseCells(cell)
                self.__setNbMineClose(cell)
                line.append(copy.copy(cell))
            self.__cellList.append( line.copy() )

    def __setCloseCells(self, cell):

        #   general:
        #   x -> h | y -> w
        #
        #   x-1y-1  x-1y    x-1y+1
        #   xy-1    xy      xy+1
        #   x+1y-1    x+1y    x+1y+1

        #   val:    xy      ->  index
        #   up:     x-1y-1  ->  index   -w  -1
        #           x-1y    ->  index   -w
        #           x-1y+1  ->  index   -w  +1
        #   same:   xy-1    ->  index       -1
        #           xy+1    ->  index       +1
        #   down:   x+1y-1  ->  index   +w  -1
        #           x+1y    ->  index   +w
        #           x+1y+1  ->  index   +w  +1

        #   table 5x6 --> index
        #     h
        #   w 0   1   2   3   4   5
        #     6   7   8   9   10  11
        #     12  13  14  15  16  17
        #     18  19  20  21  22  23
        #     24  25  26  27  28  29

        lstClose = [int]

        fl = bool((cell._id % self._width) == 0)     # if cell not full left
        fr = bool((cell._id % self._width) == (self._width-1)) # if cell not full right
        ft = bool(cell._id < self._width)           # if cell not full top
        fb = bool(cell._id >= ((self._height-1)*self._width))   # if cell not full bottom

        if not (fl | ft):   lstClose.append(cell._id-self._width-1)  # NW corner
        if not ft:          lstClose.append(cell._id-self._width)    # N corner
        if not (fr | ft):   lstClose.append(cell._id-self._width+1)  # NE corner
        if not fl:          lstClose.append(cell._id-1)    # W corner
        if not fr:          lstClose.append(cell._id+1)    # E corner
        if not (fl | fb):   lstClose.append(cell._id+self._width-1)  # SW corner
        if not fb:          lstClose.append(cell._id+self._width)    # S corner
        if not (fr | fb):   lstClose.append(cell._id+self._width+1)  # SE corner

        cell._closeCells = lstClose

    def __setNbMineClose(self, cell):
        i: int = 0
        for id in cell._closeCells:
            if id in self.__lstMine:
                i += 1
        cell._nbMineClose = i


#---| End Conditions |--------------------------------------------------------------------------------------------------

    def isWin(self):
        nbSave = 0
        nbSaveMax = (self._width * self._height) - self._nbMineTotal

        for line in self.__cellList:
            for cell in line:
                if cell._isDiscovered:
                    if cell.asExplode(): return False
                    else: nbSave += 1

        return bool(nbSave == nbSaveMax)

    def isLose(self):
        for line in self.__cellList:
            for cell in line:
                if cell.asExplode():
                    return True

        return False


#---| DEBUG ZONE |------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    def printPlayGrid(lst):
        for line in lst:
            linetext = "|"
            interline = "_"
            for cell in line:
                linetext += " " + str(cell) + (" " * (7 - len(cell))) + " |"
                interline += "_"* 10
            print(linetext)
            print(interline)

    def printEndGrid(lst):
        for line in lst:
            linetext = "|"
            linetext2 = "|"
            interline = "_"
            for cell in line:
                linetext += " " + str(cell[0]) + (" " * (5-len(str(cell[0])))) + " |"
                linetext2 += " " + str(cell[1]) + (" " * (5-len(str(cell[1])))) + " |"
                interline += "_"* 8
            print(linetext)
            print(linetext2)
            print(interline)


    h = 5
    w = 6
    nbm = 10
    test = Grid(h, w, nbm)

    test.play(1,2)
    test.play(2,0)

    printEndGrid(test.getEndingGrid())

