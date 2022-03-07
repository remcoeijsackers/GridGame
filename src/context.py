
class modal_context:
    def __init__(self, title, ctype, command=None) -> None:
        self.title: str = title
        self.ctype: str = ctype
        self.command: function = command

class unit_modal_context(modal_context):
    def __init__(self, title, ctype, unit, command=None) -> None:
        super().__init__(title, ctype, command)
        self.unit = unit
class settings_context:
    def __init__(self, var_tiles=14, var_water_clusters=2, var_trees=8, var_factories=2, var_npcs=0, var_units1=2, var_units2=2, var_boardsize=800) -> None:
        self.var_tiles= var_tiles
        self.var_water_clusters= var_water_clusters
        self.var_trees= var_trees
        self.var_factories= var_factories
        self.var_npcs= var_npcs
        self.var_units1= var_units1
        self.var_units2= var_units2
        self.var_boardsize= var_boardsize

class color_context:
    def __init__(self) -> None:
        self.board_background = '#422102'
        self.symbol_x_color = '#EE4035'
        self.symbol_tree_color = '#41701b'
        self.symbol_tree_subcolor = '#264a0a'
        self.symbol_dot_color = '#A999CC'
        self.symbol_en_color = '#EE4035'
        self.symbol_attack_dot_color = '#EE4035'
        self.green_color = '#7BC043'
        self.red_color = '#EE4035'
        self.symbol_building_color = '#E0f9FF'
        self.symbol_water_color = 'blue'
        self.black_color = '#120606'
        self.canvas_text_color = '#9363FF'
        self.range_move_color = '#93631F'
        self.gray_color = 'gray'
        self.dark_gray_color = '#333131'
        self.sub_gray_color = '#575151'