import tkinter as tk
import numpy as np

from contexts import colorContext
from src.conversion import convert_coords
from src.util import unit_thickness, symbol_thickness




def draw_tree( convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position):
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -10,
                                outline=colorContext.symbol_tree_subcolor)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -20,
                                outline=colorContext.symbol_tree_color)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -30,
                                outline=colorContext.green_color)

def draw_broken_cell(   convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=colorContext.symbol_x_color)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=colorContext.symbol_x_color)

def draw_building(   convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position, color=colorContext.symbol_building_color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_rectangle(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1], width=symbol_thickness,
                                fill=color, outline=color)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness +20,
                                fill=colorContext.sub_gray_color)                              
        canvas.create_line(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1] + symbol_size, width=symbol_thickness -30,
                                fill=colorContext.black_color)
        canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=colorContext.canvas_text_color)

def draw_square(   convert: convert_coords, canvas: tk.Canvas, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_rectangle(grid_position[0] , grid_position[1],
                                grid_position[0], grid_position[1], width=symbol_thickness +10,
                                fill=color, outline=color)

def draw_unit(   convert: convert_coords, canvas: tk.Canvas, board, symbol_size, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        mappos = convert.convert_logical_to_map(logical_position)
        health = board.gethealth(mappos)

        #Legs
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness +20,
                                fill=colorContext.sub_gray_color)
                        
        # Face                        
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1],
                                grid_position[0] + symbol_size, grid_position[1] , width=unit_thickness +10,
                                fill=color)
        #Arms
        canvas.create_line(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1] - symbol_size + 4, width=symbol_thickness -20,
                                fill=colorContext.gray_color)

        #Body
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness,
                                fill=colorContext.black_color)
        #accent body
        canvas.create_line(grid_position[0], grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness,
                                fill=colorContext.dark_gray_color)

        canvas.create_text(grid_position[0] - symbol_size + 10,
                                grid_position[1] + symbol_size, 
                                fill=colorContext.canvas_text_color, text=health)
    
def draw_dot(   convert: convert_coords, canvas: tk.Canvas, logical_position, color, width=10):
        if color == colorContext.symbol_attack_dot_color or color == colorContext.gray_color:
            width = 20
        if color == colorContext.range_move_color:
            width = 15
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=width,
                                outline=color)
