
import pandas as pd
from pandas.core.frame import DataFrame
import os 
import glob

class state:
    def __init__(self) -> None:
        self.his = []
        self.v = 0

    def save(self, board):
        self.v += 1
        board.to_pickle("saves/"+str(self.v))
        di = (self.v, board)
        self.his.append(di)

    def load(self, v) -> DataFrame:
        df2 = pd.read_pickle("saves/{}".format(v))
        return df2

    def close(self):
        saves = glob.glob('saves/*')
        for f in saves:
            os.remove(f)
        exit(0)