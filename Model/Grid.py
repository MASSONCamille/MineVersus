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

    def __init__(self, height: int, width: int, nbMine: int):
        self._height = height
        self._width = width
        self._nbMineTotal = nbMine
        self.gererateGrid()


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
                    cell.click()
                cellDetail[1] = cell.getValue()
                lstcell.append(cellDetail)
            listline.append(lstcell)
        return listline


#---| Grid generation functions |---------------------------------------------------------------------------------------

    def gererateGrid(self):
        self.__cellList = []

        nbCase = self._width * self._height
        lstMine = random.sample( list(range(0, nbCase)), self._nbMineTotal )   # generate a list with _nbMineTotal
                                                                                # position
        for i in range(0, self._height):
            line = []
            for j in range(0, self._width):
                index = j + i * self._width
                line.append(Cell(i, j, bool(index in lstMine), self.__getCloseMine(self._height, self._width, lstMine, index)))

            self.__cellList.append( line.copy() )

    def __getCloseMine(self, h, w, lstMine, index):

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

        nbClose = 0

        fl = bool((index % w) == 0)     # if cell not full left
        fr = bool((index % w) == (w-1)) # if cell not full right
        ft = bool(index < w)           # if cell not full top
        fb = bool(index >= ((h-1)*w))   # if cell not full bottom

        if not (fl | ft):   nbClose += int( (index-w-1) in lstMine )    # NW corner
        if not ft:          nbClose += int( (index-w) in lstMine )      # N corner
        if not (fr | ft):   nbClose += int( (index-w+1) in lstMine )    # NE corner
        if not fl:          nbClose += int( (index-1) in lstMine )      # W corner
        if not fr:          nbClose += int( (index+1) in lstMine )      # E corner
        if not (fl | fb):   nbClose += int( (index+w-1) in lstMine )    # SW corner
        if not fb:          nbClose += int( (index+w) in lstMine )      # S corner
        if not (fr | fb):   nbClose += int( (index+w+1) in lstMine )    # SE corner

        return nbClose


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
                linetext += " " + cell + (" " * (7 - len(cell))) + " |"
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
                linetext2 += " " + cell[1] + (" " * (5-len(cell[1]))) + " |"
                interline += "_"* 8
            print(linetext)
            print(linetext2)
            print(interline)


    h = 10
    w = 8
    nbm = 10
    test = Grid(h, w, nbm)

    test.play(1,2)
    test.play(2,1)

    printEndGrid(test.getEndingGrid())

