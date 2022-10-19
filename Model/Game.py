from Model.Grid import Grid


class Game:
    __grid: Grid = None
    _IsEnd: bool = False
    _rulling: dict[str: bool] = {
        "AutoClick0": True,
        "ClickableNumber": False,
    }

    def __init__(self, height: int, width: int, nbMine: int):
        self.__grid = Grid(height, width, nbMine)
