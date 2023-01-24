class placement_context:
    def __init__(self, mode) -> None:
        self.mode = mode

class settings_context:
    def __init__(self, var_tiles=14, var_water_clusters=2, var_trees=8, var_factories=2, var_npcs=0, var_units1=2, var_units2=2, var_boardsize=800) -> None:
        self.var_tiles= var_tiles
        self.var_water_clusters= var_water_clusters
        self.var_trees= var_trees
        self.var_factories= var_factories
        self.var_npcs= var_npcs
        self.var_units= var_units1
        self.var_units2= var_units2
        self.var_boardsize= var_boardsize
