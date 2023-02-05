import random
from src.objectmanager.objects.piece import boardItem

boardcolors = ['#C5AE6B','#C5AE5C', '#C5AF7C']

class cell(boardItem):
    def __init__(self, name = ".", stepped_on=0, loc=None) -> None:
        super().__init__()
        self.name = name
        self.walkable = True
        self.description = "a cell on the grid"
        self.stepped_on = stepped_on
        self.color = random.choice(boardcolors)
        self.loc = loc

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def set_loc(self, loc):
        self.loc = loc
        return self.loc

class broken_cell(cell):
    def __init__(self, name="x", stepped_on=0, loc=None) -> None:
        super().__init__(name, stepped_on, loc)
        self.walkable = False
        self.description = "a broken cell on the grid"
        self.destroyed = False
        


    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
