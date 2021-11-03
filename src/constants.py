from src.settings import gridsize, debug

size_of_board = 600
number_of_col_squares = gridsize.get_gridsize()
symbol_size = (size_of_board / number_of_col_squares - size_of_board / 8) / 4
symbol_thickness = 40
unit_thickness = 10