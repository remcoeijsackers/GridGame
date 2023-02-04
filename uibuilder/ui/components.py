import tkinter as tk
from PIL import ImageTk, Image
import random

from objectmanager.objects.pawn import pawn
from gamemanager.players.owners import owner
from contexts.settingscontext import  settings_context
from contexts import colorContext
import datetime

from uibuilder.ui.helpers import destroyChilds

def make_admin_card(parent, parentwindow: tk.Frame, row=0):
        destroyChilds(parent)

        admin_frame = tk.Frame(parentwindow)

        admin_frame.grid(column=0, row=row +1,sticky=tk.W)

        secrow = row + 2
        unit_name_label = tk.Label(admin_frame, text="Reset game", background=colorContext.gray_color)
        reset_game_button = tk.Button(admin_frame, text="reset", background=colorContext.red_color)
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
        destroyChilds(parent)
        parent["background"] = player.color

        panel = tk.Frame(parent, background=player.color)

        panel.grid(row=row, column=0, columnspan=6, sticky=tk.EW)

        secrow = row + 2
        turn_label = tk.Label(panel, text="{}".format(player.name), background=player.color, font=("Courier", 20))
        actions_label = tk.Label(panel, text="Actions remaining: {}".format(player.available_actions), background=player.color)
        units_label = tk.Label(panel, text= "Units: {}".format(len(player.units)), background=player.color)
        buildings_label = tk.Label(panel, text= "Buildings: {}".format(player.buildings), background=player.color)

        turn_label.grid(column=0, row=secrow, columnspan=6)
        units_label.grid(column=0, row=secrow+2, columnspan=3)
        buildings_label.grid(column=1, row=secrow+3, columnspan=3)

        actions_label.grid(column=4, row=secrow+2, columnspan=3)

def make_unit_event_card(parent: tk.Frame, unit: pawn, row):
        event_frame = tk.Frame(parent) 
        event_frame.grid(column=0, row=row, columnspan=6, sticky=tk.EW)
        scrollbar = tk.Scrollbar(event_frame)
        scrollbar.grid(column=0, row=row, sticky=tk.EW)

        mylist =  tk.Listbox(event_frame, yscrollcommand = scrollbar.set, width=60)
        for line in unit.events:
            mylist.insert(tk.END, "{}: ".format(datetime.datetime.now().time().replace(microsecond=0, second=0)) + str(line))

        mylist.grid(column=0, row=row, sticky=tk.EW, columnspan=6)

def make_gameevent_card(parentwindow, parentframe):
        #parentwindow.event_label = tk.Label(parentframe, text="Events", background=colorContext.gray_color, width=88, height=5)
        #parentwindow.event_label.pack(side='top',anchor='e')

        parentwindow.rightcontrolframeevents =tk.Frame(parentframe)
        parentwindow.rightcontrolframeevents.pack(side='top',anchor='e', fill='x')

def make_generic_event_card(parent: tk.Frame, events=None):
        destroyChilds(parent)
        event_frame = tk.Frame(parent) 
        event_frame.pack(fill='x')
        scrollbar = tk.Scrollbar(parent,orient=tk.VERTICAL) #event_frame
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        mylist =  tk.Listbox(parent, yscrollcommand = scrollbar.set, width=60) #event_frame
        if events != None:
                for line in events:
                        mylist.insert(tk.END, "{}: ".format(datetime.datetime.now().time().replace(microsecond=0, second=0)) + str(line))

        mylist.pack(fill='x')

def make_unit_card(srcparent, parent: tk.Frame, unit: pawn, row=0):
        destroyChilds(parent)
        main_unit_frame = tk.Frame(parent)
        main_unit_frame.grid(column=0, row=row)

        unit_details_frame = tk.Frame(main_unit_frame)
        unit_details_frame.grid()

        unit_frame = tk.Frame(unit_details_frame)
        unit_frame.grid(column=2, row=row) #, sticky=tk.W

        unit_image_frame = tk.Frame(unit_details_frame, relief=tk.RIDGE, background=colorContext.black_color)
        unit_image_frame.grid(column=0, row=row, columnspan=2, sticky=tk.W)

        img = Image.open(unit.image)
        img = img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(unit_image_frame, image = img, background=colorContext.black_color)
        panel.image = img    
        panel.grid(row=0, column=0, sticky=tk.W)

        unit_name_label = tk.Label(unit_frame, text=unit.fullname[:30])
        #unit_age_label = tk.Label(unit_frame, text="Age: {}".format(unit.age))
        unit_health_label = tk.Label(unit_frame, text="Health: {}".format(unit.health))
        unit_attack_label = tk.Label(unit_frame, text="Attack: {}".format(unit.strength))
        unit_range_label = tk.Label(unit_frame, text="Range: {}".format(unit.range))

        unit_equipment_label_header = tk.Label(unit_frame, text="Armor", background=colorContext.symbol_tree_color)
        unit_equipment_label_head = tk.Label(unit_frame, text="Head: {}".format(unit.equipment.kit["head"]))
        unit_equipment_label_torso = tk.Label(unit_frame, text="Body: {}".format(unit.equipment.kit["body"]))
        unit_equipment_label_legs = tk.Label(unit_frame, text="Legs: {}".format(unit.equipment.kit["legs"]))

        unit_equipment_label_weapon_header = tk.Label(unit_frame, text="Weapons",  background=colorContext.red_color)
        unit_equipment_label_melee = tk.Label(unit_frame, text="Melee: {}".format(unit.equipment.kit["melee"]))

        unit_name_label.grid(column=0, row=0, sticky=tk.W)
        unit_health_label.grid(column=0, row=1, sticky=tk.W)
        unit_attack_label.grid(column=0, row=2, sticky=tk.W)
        unit_range_label.grid(column=0, row=3, sticky=tk.W)

        #unit_age_label.grid(column=1, row=0, sticky=tk.E)
        unit_equipment_label_header.grid(column=1, row=0, sticky=tk.EW)
        unit_equipment_label_head.grid(column=1, row=1, sticky=tk.E)
        unit_equipment_label_torso.grid(column=1, row=2, sticky=tk.E)
        unit_equipment_label_legs.grid(column=1, row=3, sticky=tk.E )

        unit_equipment_label_weapon_header.grid(column=3, row=0, sticky=tk.EW)
        unit_equipment_label_melee.grid(column=3, row=1, sticky=tk.E)

        unit_event_Frame = tk.Frame(main_unit_frame)
        unit_event_Frame.grid(column=0, row=10)
        make_unit_event_card(main_unit_frame, unit, 20)
        
def initilise_settings(parent, settings: settings_context, home_init_func):
        settings_frame = tk.Frame(parent, padx= 100, pady=100)
        header_label_settings = tk.Label(settings_frame, text="Settings", font=("Courier", 44))
        seed_entry = tk.Entry(settings_frame, width=15)
        seed_entry.insert(0, '{}'.format(random.randint(0, 9438132)))
        #seed_entry_label = tk.Label(settings_frame, text="Seed", width=15)
        tiles = tk.Scale(settings_frame, from_=6, to=20, orient=tk.HORIZONTAL, length=300, label="Tiles on the board (value x2)")
        tiles.set(settings.var_tiles)
        boardsize = tk.Scale(settings_frame, from_=300, to=1200, orient=tk.HORIZONTAL, length=300, label="Size of the board (value x2)")
        boardsize.set(settings.var_boardsize)
        total_tiles_label = tk.Label(settings_frame, text="total tiles: {}".format(tiles.get() * tiles.get()), width=15)
        water_clusters = tk.Scale(settings_frame, from_=0, to=3, orient=tk.HORIZONTAL, length=150, label="Lakes")
        water_clusters.set(settings.var_water_clusters)
        trees = tk.Scale(settings_frame, from_=0, to=10, orient=tk.HORIZONTAL, length=150, label="Trees")
        trees.set(settings.var_trees)
        factories = tk.Scale(settings_frame, from_=0, to=5, orient=tk.HORIZONTAL, length=150, label="Factories")
        factories.set(settings.var_factories)
        #npcs = tk.Scale(settings_frame, from_=0, to=5, orient=tk.HORIZONTAL, length=150, label="count of NPC's")
        #npcs.set(settings.var_npcs)
        units1 = tk.Scale(settings_frame, from_=1, to=10, orient=tk.HORIZONTAL, length=300, label="Units per player")
        units1.set(settings.var_units)
               
        min_size_needed = tiles.get() + water_clusters.get() * 5  + trees.get() + factories.get() +  units1.get()  + 10

        total_objects_label = tk.Label(settings_frame, text="Total objects: {}".format(min_size_needed), width=15)

        def check_settings_possible():
                watr = int(water_clusters.get())
                total_tiles = tiles.get() * tiles.get()
                min_size_needed = tiles.get() + watr * 5  + trees.get() + factories.get() +  units1.get() +  5
                if min_size_needed > total_tiles:
                    tiles.set(min_size_needed)
                    total_tiles_label['text'] = "Total tiles: {}".format(total_tiles)
                    return min_size_needed

        def validate():
            check_settings_possible()
            settings.var_tiles = tiles.get()
            settings.var_water_clusters = water_clusters.get()
            settings.var_trees = trees.get()
            settings.var_factories = factories.get()

            settings.var_units = units1.get()
            settings.var_boardsize = boardsize.get()
            settings_frame.destroy()
            home_init_func(settings)

        header_label_settings.grid(column=0, row=0, columnspan=4)

        units1.grid(column=0, row=1,pady=10, padx=10, columnspan=4)

        tiles.grid(column=0, row=4, columnspan=4, pady=10, padx=10)
        boardsize.grid(column=0, row=5, columnspan=4, pady=10, padx=10)

        trees.grid(column=0, row=6, pady=10, padx=10)
        water_clusters.grid(column=1, row=6, pady=10, padx=10)

        factories.grid(column=0, row=7,  pady=10, padx=10)

        total_tiles_label.grid(column=0, row=10,  pady=10, padx=10)
        total_objects_label.grid(column=1, row=10,  pady=10, padx=10)

        object_placement_mode_label = tk.Label(settings_frame, text="Object placement mode", width=30)
        unit_placement_mode_label = tk.Label(settings_frame, text="Unit placement mode", width=30)

        OPTIONS = [
                    "random",
                    "rigid",
                    ] 
                
        unit_placement_mode_variable = tk.StringVar(settings_frame)
        unit_placement_mode_variable.set(OPTIONS[0])

        unit_placement_mode_label.grid(column=0, row=8)
        unit_placement_mode = tk.OptionMenu(settings_frame, unit_placement_mode_variable, *OPTIONS)
        unit_placement_mode.grid(column=1, row=8)

        object_placement_variable = tk.StringVar(settings_frame)
        object_placement_variable.set(OPTIONS[0])

        object_placement_mode_label.grid(column=0, row=9)        
        object_placement_mode = tk.OptionMenu(settings_frame, object_placement_variable, *OPTIONS)
        object_placement_mode.grid(column=1, row=9)


        back_home_button = tk.Button(
                settings_frame,
                text='back home',
                command=validate, background=colorContext.board_background)

        back_home_button.grid(column=0, row=12, columnspan=4)
        
        settings_frame.pack()