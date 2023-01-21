import tkinter as tk
from PIL import ImageTk, Image
import random

from src.objects import pawn
from src.controller import owner
from src.context import color_context, modal_context, settings_context
from src.conversion import convert_coords
from src.util import unit_thickness, symbol_thickness
import datetime
colors = color_context()

def make_admin_card(parent, parentwindow: tk.Frame, row=0):
        parentwindow.children.clear()

        admin_frame = tk.Frame(parentwindow, relief=tk.RIDGE)

        admin_frame.grid(column=0, row=row +1,sticky=tk.W)

        secrow = row + 2
        unit_name_label = tk.Label(admin_frame, text="Reset game", background=colors.gray_color)
        reset_game_button = tk.Button(admin_frame, text="reset", background=colors.red_color)
        reset_game_button.grid(column=0, row=0, columnspan=parent.max_ui_columns)
        unit_health_label = tk.Label(admin_frame, text="Admin Action")
        unit_attack_label = tk.Label(admin_frame, text="Admin Action")
        unit_range_label = tk.Label(admin_frame, text="Admin Action")
        show_stepped_tiles_button = tk.Button(admin_frame, text="show prev. moves", command=parent.show_stepped_tiles)


        unit_name_label.grid(column=0, row=secrow, sticky=tk.W)
        reset_game_button.grid(column=1, row=secrow, sticky=tk.E)

        unit_health_label.grid(column=0, row=secrow+1, sticky=tk.W)
        show_stepped_tiles_button.grid(column=1, row=secrow+1,sticky=tk.E)

        unit_attack_label.grid(column=0, row=secrow+2, sticky=tk.W)
        unit_range_label.grid(column=0, row=secrow+3, sticky=tk.W)


        reset_game_button.bind('<Button-1>', parent.admin_reset_board)

def make_player_card(parent: tk.Frame, player: owner, row= 0):
        parent.children.clear()

        panel = tk.Frame(parent,relief=tk.RIDGE, background=player.color)

        panel.grid(row=row, column=0,columnspan=6)

        secrow = row + 2
        turn_label = tk.Label(panel, text="{}".format(player.name), background=player.color)
        actions_label = tk.Label(panel, text="Actions remaining: {}".format(player.available_actions + 1), background=player.color)
        buildings_label = tk.Label(panel, text= "Units: {}, Buildings: {}".format(len(player.units), player.buildings), background=player.color)

        turn_label.grid(column=0, row=secrow, columnspan=6)
        actions_label.grid(column=0, row=secrow+1)
        buildings_label.grid(column=0, row=secrow+2)

def make_unit_event_card(parent: tk.Frame, unit: pawn, row=0):
        parent.children.clear()
        event_frame = tk.Frame(parent, relief=tk.RIDGE)
        event_frame.grid(column=0, row=row, sticky=tk.EW, columnspan=6)
        scrollbar = tk.Scrollbar(event_frame)
        scrollbar.grid(column=0, row=row, sticky=tk.EW, columnspan=6)

        mylist =  tk.Listbox(parent, yscrollcommand = scrollbar.set )
        for line in unit.events:
            mylist.insert(tk.END, "{}: ".format(datetime.datetime.now().time().replace(microsecond=0, second=0)) + str(line))

        mylist.grid(column=0, row=row, columnspan=6,sticky=tk.EW)

def make_unit_card(srcparent, parent: tk.Frame, unit: pawn, row=0):
        parent.children.clear()
        unit_frame = tk.Frame(parent, relief=tk.RIDGE)
        unit_frame.grid(column=2, row=row,sticky=tk.W)
        unit_image_frame = tk.Frame(parent, relief=tk.RIDGE, background=colors.black_color)
        unit_image_frame.grid(column=0, row=row, columnspan=2, sticky=tk.W)
        unit_event_Frame = tk.Frame(parent, relief=tk.RIDGE, background=colors.ui_background)
        unit_event_Frame.grid(column=0, row=row+5,sticky=tk.EW)

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
        make_unit_event_card(unit_event_Frame, unit, 10)
        
def initilise_settings(parent, settings: settings_context, home_init_func):
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
        placementRandom = tk.Checkbutton(settings_frame)
        placementRigid = tk.Checkbutton(settings_frame)
        
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
        placementRandom.grid(column=0, row=10)
        placementRigid.grid(column=0, row=11)
        seed_entry.grid(column=1, row=12, pady=10, padx=10)

        back_home_button = tk.Button(
                settings_frame,
                text='back home',
                command=validate, background=colors.board_background)

        back_home_button.grid(column=0, row=9, columnspan=4)
        
        settings_frame.pack()