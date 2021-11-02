import numpy as np

from src.constants import size_of_board
from src.util import colsr, colsc

class convert_coords:
    """
    Converts tkinter canvas coordinates to pandas grid coordinates, and vice versa.
    """
    def __init__(self, gridsize) -> None:
        self.gridsize = gridsize
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / self.gridsize) * logical_position + size_of_board / (self.gridsize * 2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / self.gridsize), dtype=int)

    def convert_logical_to_map(self, logical_postion):
        alp = [i for i in logical_postion]
        letter = colsr.get(alp[0])
        map_position = (alp[1], letter)
        return map_position
        
    def convert_map_to_logical(self, map_position):
        number = colsc.get(map_position[1])
        log_pos = np.array([number, map_position[0]], dtype=int)
        return log_pos