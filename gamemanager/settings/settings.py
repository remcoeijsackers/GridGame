debug = True
class gridsizing:
    def __init__(self) -> None:
        self.gridsize = 10

    def set_gridsize(self, size):
        self.gridsize = size

    def get_gridsize(self) -> int:
        return self.gridsize 

gridsize = gridsizing()


class symbolsizing:
    def __init__(self) -> None:
        self.col_squares = gridsize.get_gridsize()
    
    def get_symbolsize(self, boardsize) -> int:
        return (boardsize / self.col_squares - boardsize / 8) / 4

symbolsize = symbolsizing()