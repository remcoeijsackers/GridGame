import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import random

from src.objects import unit
from src.controller import owner
from src.context import color_context, modal_context, settings_context
from src.conversion import convert_coords
from src.util import unit_thickness, symbol_thickness

colors = color_context()

class uihandler:

    def make_player_card(self, parent: tk.Frame, player: owner, row= 0):
        parent.children.clear()
        panel = tk.Frame(parent,relief=tk.RIDGE, background=player.color)
        panel.grid(row=0,column=0, columnspan=6,sticky=tk.EW)
        turn_label = tk.Label(panel, text="{}".format(player.name), background=player.color)
        actions_label = tk.Label(panel, text="Actions remaining: {}".format(player.available_actions + 1), background=player.color)
        buildings_label = tk.Label(panel, text= "Units: {}, Buildings: {}".format(len(player.units), player.buildings), background=player.color)

        turn_label.grid(column=0, row=1, columnspan=6)
        actions_label.grid(column=0, row=2, columnspan=6)
        buildings_label.grid(column=0, row=3, columnspan=6)

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

    def initilise_settings(self, parent, settings: settings_context, home_init_func):
        settings_frame = tk.Frame(parent, padx= 100, pady=100, relief=tk.RIDGE)
        header_label_settings = tk.Label(settings_frame, text="Settings", font=("Courier", 44))
        seed_entry = tk.Entry(settings_frame, width=15)
        seed_entry.insert(0, '{}'.format(random.randint(0, 9438132)))
        seed_entry_label = tk.Label(settings_frame, text="Seed", width=15)
        tiles = tk.Scale(settings_frame, from_=6, to=20, orient=tk.HORIZONTAL, length=300, label="tiles in the game board (value x2)")
        tiles.set(settings.var_tiles)
        boardsize = tk.Scale(settings_frame, from_=300, to=1200, orient=tk.HORIZONTAL, length=300, label="size of the game board (value x2)")
        boardsize.set(settings.var_boardsize)
        total_tiles_label = tk.Label(settings_frame, text="total tiles: {}".format(tiles.get() * tiles.get()), width=15)
        water_clusters = tk.Scale(settings_frame, from_=0, to=3, orient=tk.HORIZONTAL, length=150, label="count of lakes")
        water_clusters.set(settings.var_water_clusters)
        trees = tk.Scale(settings_frame, from_=0, to=10, orient=tk.HORIZONTAL, length=150, label="count of trees")
        trees.set(settings.var_trees)
        factories = tk.Scale(settings_frame, from_=0, to=5, orient=tk.HORIZONTAL, length=150, label="count of factories")
        factories.set(settings.var_factories)
        npcs = tk.Scale(settings_frame, from_=0, to=5, orient=tk.HORIZONTAL, length=150, label="count of NPC's")
        npcs.set(settings.var_npcs)
        units1 = tk.Scale(settings_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=300, label="Units p1")
        units1.set(settings.var_units1)
        units2 = tk.Scale(settings_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=300, label="Units p2")
        units2.set(settings.var_units2)
        
        min_size_needed = tiles.get() + water_clusters.get() * 5  + trees.get() + factories.get() + npcs.get() + units1.get() + units2.get() + 10

        total_objects_label = tk.Label(settings_frame, text="total objects: {}".format(min_size_needed), width=15)

        def check_settings_possible():
                watr = int(water_clusters.get())
                total_tiles = tiles.get() * tiles.get()
                min_size_needed = tiles.get() + watr * 5  + trees.get() + factories.get() + npcs.get() + units1.get() + units2.get() + 5
                if min_size_needed > total_tiles:
                    tiles.set(min_size_needed)
                    total_tiles_label['text'] = "total tiles: {}".format(total_tiles)
                    return min_size_needed
        def validate():
            check_settings_possible()
            settings.var_tiles = tiles.get()
            settings.var_water_clusters = water_clusters.get()
            settings.var_trees = trees.get()
            settings.var_factories = factories.get()
            settings.var_npcs = npcs.get()
            settings.var_units1 = units1.get()
            settings.var_units2 = units2.get()
            settings.var_boardsize = boardsize.get()
            settings_frame.destroy()
            home_init_func(settings)

        header_label_settings.grid(column=0, row=0, columnspan=4)

        units1.grid(column=0, row=1,pady=10, padx=10, columnspan=4)
        units2.grid(column=0, row=2,pady=10, padx=10, columnspan=4)

        tiles.grid(column=0, row=4, columnspan=4, pady=10, padx=10)
        boardsize.grid(column=0, row=5, columnspan=4, pady=10, padx=10)

        trees.grid(column=0, row=6, pady=10, padx=10)
        water_clusters.grid(column=1, row=6, pady=10, padx=10)

        factories.grid(column=0, row=7,  pady=10, padx=10)
        npcs.grid(column=1, row=7, pady=10, padx=10)

        total_tiles_label.grid(column=0, row=8,  pady=10, padx=10)
        total_objects_label.grid(column=1, row=8,  pady=10, padx=10)

        seed_entry_label.grid(column=0, row=9,  pady=10, padx=10)
        seed_entry.grid(column=1, row=9, pady=10, padx=10)

        back_home_button = tk.Button(
                settings_frame,
                text='back home',
                command=validate, background=colors.board_background)

        back_home_button.grid(column=0, row=9, columnspan=4)
        
        settings_frame.pack()
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
