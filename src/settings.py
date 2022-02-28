debug = True
class gridsizing:
    def __init__(self) -> None:
        self.gridsize = 10

    def set_gridsize(self, size):
        self.gridsize = size

    def get_gridsize(self) -> int:
        return self.gridsize 

gridsize = gridsizing()
