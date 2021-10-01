import pandas as pd
from pandas.core.frame import DataFrame

from util import cols 
from objects import cell

class grid:
    def __init__(self) -> None:
        self.base_grid = []

    def setup(self) -> DataFrame:
        grd = []
        [grd.append(cell()) for i in range(10)]
        [self.base_grid.append(grd) for i in range(10)]
        
        df = pd.DataFrame(self.base_grid, columns=cols)
        return df



    
