import pandas as pd
from pandas.core.frame import DataFrame

from util import cols,gridsize,fullcols
from objects import cell

class grid:
    """
    Creates the dataframe to be used as game board.
    """
    def __init__(self) -> None:
        self.base_grid = []

    def setup(self) -> DataFrame:
        grd = []
        [grd.append(cell()) for i in range(gridsize)]
        [self.base_grid.append(grd) for i in range(gridsize)]
        
        df = pd.DataFrame(self.base_grid, columns=fullcols[:gridsize])
        return df



    
