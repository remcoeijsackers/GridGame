import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

from src.objects import unit
from src.context import color_context, modal_context
from src.conversion import convert_coords
from src.util import unit_thickness, symbol_thickness

colors = color_context()

class uihandler:
    def make_unit_card(self, parent: tk.Frame, unit: unit, row=0):
        parent.children.clear()
        unit_frame = tk.Frame(parent, relief=tk.RIDGE)
        unit_frame.grid(column=2, row=row,sticky=tk.W)
        unit_image_frame = tk.Frame(parent, relief=tk.RIDGE, background=colors.black_color)
        unit_image_frame.grid(column=0, row=row, columnspan=2, sticky=tk.W)

        img = Image.open(unit.image)
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(unit_image_frame, image = img, background=colors.black_color)
        panel.image = img    
        panel.grid(row=0, column=0, sticky=tk.W)

        unit_name_label = tk.Label(unit_frame, text=unit.fullname)
        unit_age_label = tk.Label(unit_frame, text="Age: {}".format(unit.age))
        unit_health_label = tk.Label(unit_frame, text="Health: {}".format(unit.health))
        unit_attack_label = tk.Label(unit_frame, text="Attack: {}".format(unit.strength))
        unit_range_label = tk.Label(unit_frame, text="Range: {}".format(unit.range))
        unit_equipment_label = tk.Label(unit_frame, text="Equipment: {}".format(unit.equipment))

        unit_name_label.grid(column=0, row=0, sticky=tk.W)
        unit_age_label.grid(column=1, row=0, sticky=tk.E)
        unit_health_label.grid(column=0, row=1, sticky=tk.W)
        unit_attack_label.grid(column=0, row=2, sticky=tk.W)
        unit_range_label.grid(column=0, row=3, sticky=tk.W)
        unit_equipment_label.grid(column=0, row=4, sticky=tk.W)

class modal_popup(tk.Toplevel):

    def __init__(self, original, context: modal_context):

        self.original_frame = original
        tk.Toplevel.__init__(self)

        self.transient(self.original_frame.window)
        self.geometry("260x210")
        self.lift()

        title = tk.Label(self, text = context.title)
        title.grid(row=0, column=0, sticky=tk.EW)

        if context.ctype == "unit":
            uihandler().make_unit_card(self, context.unit, row=0)

        if context.command:
            context_btn = tk.Button(self, text=context.ctype, command=context.command)
            context_btn.grid(row=3, column=0)

    def on_close(self):
        self.destroy()
        self.original_frame.window.update()
        self.original_frame.window.deiconify()


class painter:
    def draw_tree(self, convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position):
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -10,
                                outline=colors.symbol_tree_subcolor)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -20,
                                outline=colors.symbol_tree_color)
        canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -30,
                                outline=colors.green_color)

    def draw_broken_cell(self, convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=colors.symbol_x_color)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=colors.symbol_x_color)

    def draw_building(self, convert: convert_coords, canvas: tk.Canvas, symbol_size, logical_position, color=colors.symbol_building_color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_rectangle(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1], width=symbol_thickness,
                                fill=color, outline=color)
        canvas.create_line(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=colors.black_color)
        canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=colors.canvas_text_color)

    def draw_square(self, convert: convert_coords, canvas: tk.Canvas, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_rectangle(grid_position[0] , grid_position[1],
                                grid_position[0], grid_position[1], width=40,
                                fill=color, outline=color)

    def draw_unit(self, convert: convert_coords, canvas: tk.Canvas, board, symbol_size, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        mappos = convert.convert_logical_to_map(logical_position)
        health = board.gethealth(mappos)
        canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness,
                                fill=color)
        canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=colors.canvas_text_color, text=health)
    
    def draw_dot(self, convert: convert_coords, canvas: tk.Canvas, logical_position, color):
        width = 10
        if color == colors.symbol_attack_dot_color or color == colors.gray_color:
            width = 20
        if color == colors.range_move_color:
            width = 15
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=width,
                                outline=color)
