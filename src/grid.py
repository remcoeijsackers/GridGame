import pandas as pd
from pandas.core.frame import DataFrame

from src.util import fullcols
from src.objects import cell

class grid:
    """
    Creates the dataframe to be used as game board.
    """
    def __init__(self, gridsize) -> None:
        self.gridsize = gridsize
        self.base_grid = []

    def setup(self) -> DataFrame:
        grd = []
        [grd.append(cell()) for i in range(self.gridsize)]
        [self.base_grid.append(grd) for i in range(self.gridsize)]
        
        df = pd.DataFrame(self.base_grid, columns=fullcols[:self.gridsize])
        return df



    
