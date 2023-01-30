import numpy as np

from src.util import  colsr, colsc, topL, topR, bottomL, bottomR, top, bottom, left, right
import dataclasses 

@dataclasses.dataclass
class eventStub:
    x: float
    y: float

class convert_coords:
    """
    Converts tkinter canvas coordinates to pandas grid coordinates, and vice versa.
    """
    def __init__(self, gridsize, boardsize) -> None:
        self.gridsize = gridsize
        self.boardsize = boardsize

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        pos = (self.boardsize / self.gridsize) * logical_position + self.boardsize / (self.gridsize * 2)
        return pos

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (self.boardsize / self.gridsize), dtype=int)

    def convert_logical_to_map(self, logical_postion):
        alp = [i for i in logical_postion]
        letter = colsr().get(alp[0])
        map_position = (alp[1], letter)
        return map_position
        
    def convert_map_to_logical(self, map_position):
        number = colsc().get(map_position[1])
        log_pos = np.array([number, map_position[0]], dtype=int)
        return log_pos
    
    def convert_action_str_to_logical(self, unit, action):
        loc = unit.loc
        def getLoc():
            if action == "up":
                if loc[0] != 0:
                    locstub = (loc[0] -1, loc[1])
            if action == "down":
                if loc[0] != max(self.boardsize):
                    locstub = (loc[0] + 1, loc[1])
            return locstub
        return self.convert_map_to_logical(getLoc())

    def convert_action_str_to_grid_position(self, unit, action):
        loc = unit.loc
        def getLoc():
            if action == "up":
                if loc[0] != 0:
                    locstub = (loc[0] -1, loc[1])
            if action == "down":
                #if loc[0] != max(self.boardsize):
                locstub = (loc[0] + 1, loc[1])
            return locstub
        return self.convert_logical_to_grid_position(self.convert_map_to_logical(getLoc()))

    def convert_action_str_to_position_event(self, unit, action):
        loc = unit.loc
        print("calling: convert_action_str_to_position_event")
        print(f"action: {action}")

        def getLoc():
            if action == "top":

                return top(loc)
            if action == "bottom":
                #locstub = (loc[0] + 1, loc[1])
                return bottom(loc)
            if action == "left":
                #locstub = (loc[0], colsr().get(colsc().get(loc[1]) -1))
                return left(loc)
            if action == "right":
                #locstub = (loc[0], colsr().get(colsc().get(loc[1]) +1))
                return right(loc)
            if action == "topleft":
                return topL(loc)
            if action == "topright":
                return topR(loc)
            if action == "bottomleft":
                return bottomL(loc)
            if action == "bottomright":
                return bottomR(loc)


        gridpos = self.convert_logical_to_grid_position(self.convert_map_to_logical(getLoc()))
        event = eventStub(gridpos[0], gridpos[1])
        return event

    def convert_map_to_position_event(self, map_position):
        gridpos = self.convert_logical_to_grid_position(self.convert_map_to_logical(map_position))
        event = eventStub(gridpos[0], gridpos[1])
        return event