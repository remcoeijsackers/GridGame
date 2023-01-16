from turtle import back
from src.util import placeipRigid
import random

import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename

from src.unitgen import unitgenerator
from src.manager import manager, unitcontroller, placement
from src.util import placeip
from src.state import state
from src.objects import broken_cell, player, cell, scenery, unit, building, enemy, water, tree
from src.grid import grid
from src.settings import debug, gridsize, symbolsize
from src.conversion import convert_coords
from src.controller import controller, owner
from src.context import modal_context, settings_context, color_context, unit_modal_context
from src.ui import uihandler, modal_popup, painter

convert = any
colors = color_context()
ui = uihandler()
brd = manager()   
st = state()
control = unitcontroller()
unithandler = unitgenerator()
game_settings = settings_context()

class game():
    """
    Ties the dataframe game backend to a visual frontend.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('GridGame')
        self.window.minsize(width=1000, height=600)
        self.itemPlacement = "rigid"

        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar)

        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_game)
        filemenu.add_command(label="Exit")

        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        self.initialise_home(game_settings)

    def initialise_home(self, settings: settings_context):
            self.home_frame = tk.Frame(self.window, padx= 100, pady=100, relief=tk.RIDGE, width=1000, height=600)
            header_label = tk.Label(self.home_frame, text="GridGame", font=("Courier", 44))

            entry_player_one = tk.Entry(self.home_frame)
            entry_player_one.insert(0, 'player one')
            entry_player_one['background'] = 'orange'

            entry_player_two = tk.Entry(self.home_frame)
            entry_player_two.insert(0, 'player two')
            entry_player_two['background'] = 'blue'

            def change_color_p1():
                colors = askcolor(title="Tkinter Color Chooser")
                entry_player_one.configure(bg=colors[1])
                return colors[1]
    
            def change_color_p2():
                colors = askcolor(title="Tkinter Color Chooser")
                entry_player_two.configure(bg=colors[1])
                return colors[1]
    
            def get_input():
                p1name = entry_player_one.get()
                p2name = entry_player_two.get()
                return p1name, p2name 
            
            def start_game():
                global convert
                p = get_input()
                pl1 = owner(p[0], entry_player_one['background'])
                pl2 = owner(p[1], entry_player_two['background'])
                self.gridsize = settings.var_tiles
    
                gridsize.set_gridsize(self.gridsize)
                convert = convert_coords(self.gridsize, settings.var_boardsize)
                brd.set_board(grid(self.gridsize).setup())
                self.initialise_game(pl1,pl2, settings)
                self.home_frame.destroy()
            
            def open_settings():
                ui.initilise_settings(self.window, settings, self.initialise_home)
                self.home_frame.destroy()
            
            b0 = tk.Button(
                self.home_frame,
                text='Select a Color for p1',
                command=change_color_p1, background=colors.board_background)
            b1 = tk.Button(
                self.home_frame,
                text='Select a Color for p2',
                command=change_color_p2, background=colors.board_background)

            b2 = tk.Button(self.home_frame, text="Start Game", command=start_game, background=colors.board_background)
            settings_button = tk.Button(self.home_frame, text="Settings",command=open_settings,background=colors.board_background)

            header_label.grid(column=0, row=0, columnspan=3)
            entry_player_one.grid(column=0, row=1)
            entry_player_two.grid(column=0, row=2)

            b0.grid(column=1, row=1)
            b1.grid(column=1, row=2)
            settings_button.grid(column=0, row=3, columnspan=3)

            b2.grid(column=0, columnspan=3, pady=10, padx=10)
            self.home_frame.pack()

    def initialise_game(self, player_one, player_two, settings: settings_context):
        self.boardsize = settings.var_boardsize
        self.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        self.player_one = player_one
        self.player_two = player_two
        self.show_stepped_on_tiles = False

        self.game_controller = controller(player_one, player_two)

        self.statusbar = tk.Label(self.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.window, width=settings.var_boardsize, height=settings.var_boardsize, background=colors.board_background)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = tk.Canvas(self.window, bd=1)
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Player info", background=colors.black_color)

        self.player_box = tk.Frame(self.ui,background=colors.black_color)

        self.control_label = tk.Label(self.ui, text="Controls", background=colors.black_color)
        self.mode_label = tk.Label(self.ui, text="Select and move Mode", background=colors.green_color)
        self.action_details_label = tk.Label(self.ui, text="Action details")

        self.move_button = tk.Button(self.ui, text="Select move")
        self.inspect_button = tk.Button(self.ui, text="Inspect Cell")
        self.melee_attack_button = tk.Button(self.ui, text="Melee Attack")
        self.show_stepped_tiles_button = tk.Button(self.ui, text="show stepped tiles", command=self.show_stepped_tiles)
        self.padding_label1 = tk.Label(self.ui, text="")
        self.padding_label2 = tk.Label(self.ui, text="")

        self.unit_header_label = tk.Label(self.ui, text="Controlling Unit Info", background=colors.black_color)
        self.unit_box = tk.Frame(self.ui, relief=tk.RIDGE)
        self.unit_box.grid(column=0, row=14,sticky=tk.W)

        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.player_box.grid(column=0, row=1,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.control_label.grid(column=0, row=5,sticky=tk.EW, columnspan = self.max_ui_columns)
        self.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.move_button.grid(column=0, row=7, sticky=tk.W, columnspan = 3)
        self.inspect_button.grid(column=1, row=7, sticky=tk.E, columnspan = 2)
        self.melee_attack_button.grid(column=3, row=7, sticky=tk.EW, columnspan = 3)

        #self.show_stepped_tiles_button.grid(column=0,sticky=tk.EW,  row=9, columnspan = self.max_ui_columns)
        self.action_details_label.grid(column=0, row=10,sticky=tk.W, padx=5, pady=5,columnspan = 3)

        self.padding_label1.grid(column=0, row=11, sticky=tk.W, columnspan = 4)
        self.padding_label2.grid(column=0, row=12, sticky=tk.W, columnspan = 4)

        self.unit_header_label.grid(column=0, row=13, sticky=tk.EW, columnspan = 6)

        self.ui.pack(side='right',anchor=tk.NW,expand=True,fill='both')
        
        self.move_button.bind('<Button-1>', self.switch_mode_selectmove)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)
        self.melee_attack_button.bind('<Button-1>', self.switch_mode_melee_attack)
        self.canvas.bind('<Button-1>', self.select_move_click)

        for i in range(settings.var_units1):
            soldier = player("P1-{}".format(i))
            soldier.fullname = unithandler.get_name()
            soldier.owner = self.player_one
            soldier.set_image(unithandler.get_image())
            soldier.set_age(unithandler.get_age())
            self.player_one.units.append(soldier)
            if self.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "top")

        for i in range(settings.var_units2):
            soldier = player("P2-{}".format(i))
            soldier.fullname = unithandler.get_name()
            soldier.owner = self.player_two
            soldier.set_image(unithandler.get_image())
            soldier.set_age(unithandler.get_age())
            self.player_two.units.append(soldier)
            if self.itemPlacement == "rigid":
                placeipRigid(brd.board, soldier, "bottom")
        
        for i in range(settings.var_water_clusters):
            water_clustr = water("W")
            brd.placeclus(water_clustr)

        for i in range(settings.var_factories):
            fct = building("F")
            placeip(brd.board, fct)

        for i in range(settings.var_npcs):
            npc = enemy("NPC")
            npc.fullname = unithandler.get_name()
            npc.set_image(unithandler.get_image())
            npc.set_age(unithandler.get_age())
            placeip(brd.board, npc)
 
        for i in range(settings.var_trees):
            makore = tree("T")
            placeip(brd.board, makore)

        
        self.controlling_player = self.player_one
        self.selected = False
        self.selected_unit = self.controlling_player.units[0]

        ui.make_player_card(self.player_box, self.controlling_player)
        ui.make_unit_card(self.unit_box,self.selected_unit)

        self.draw_board_and_objects(brd)
        self.draw_possible_moves(self.selected_unit)

    def mainloop(self):
        """
        Runs the tkinter application.
        """
        self.window.mainloop()

    def show_stepped_tiles(self):
        if not self.show_stepped_on_tiles:
            self.show_stepped_on_tiles = True
        else:
            self.show_stepped_on_tiles = False
            self.reset(self.selected_unit.loc,type="soft")

    def switch_mode_inspect(self, event):
        """
        Switches the control mode to inspecting grid elements.
        """
        self.mode_label['text'] = "Inspect Mode"
        self.mode_label['background'] = colors.green_color
        self.canvas.bind('<Button-1>', self.inspect_click)

    def switch_mode_selectmove(self, event):
        """
        Switches the control mode to selecting and moving owned units.
        """
        self.mode_label['text'] = "Select and move Mode"
        self.mode_label['background'] = colors.green_color
        self.canvas.bind('<Button-1>', self.select_move_click)


    def switch_mode_melee_attack(self, event):
        """
        Switches the control mode to attacking with the selected unit.
        """
        self.mode_label['text'] = "Melee Attack Mode"
        self.mode_label['background'] = colors.red_color
        self.canvas.bind('<Button-1>', self.melee_attack_click)

    def get_event_info(self, event):
        """
        Changes the labels text to reflect the selected unit/cell/action
        """
        self.statusbar['text'] = " Location: {} | Steps: {} | Description: {}".format(event, control.count(self.selected_unit, event),brd.explain(event))

    def draw_board_and_objects(self, boardmanager: manager):
        """
        Cleans the board, and draws are elements in the dataframe.
        """
        def cleanup_func(obj):
            boardmanager.board.at[obj.loc[0], obj.loc[1]] = cell()
            if obj in self.player_one.units:
                self.player_one.units.remove(obj)
            if obj in self.player_two.units:
                self.player_two.units.remove(obj)

        for i in range(self.gridsize):
            self.canvas.create_line((i + 1) * self.boardsize / self.gridsize, 0, (i + 1) * self.boardsize / self.gridsize, self.boardsize)

        for i in range(self.gridsize):
            self.canvas.create_line(0, (i + 1) * self.boardsize / self.gridsize, self.boardsize, (i + 1) * self.boardsize / self.gridsize)
        
        # Changes tiles color after movement slightly
        for obj in boardmanager.get_all_clean_cells(brd.board):
            painter().draw_square(convert,self.canvas,convert.convert_map_to_logical(obj.loc),obj.color)

        for obj in boardmanager.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, water):
                painter().draw_square(convert,self.canvas,convert.convert_map_to_logical(obj.loc),obj.color)
                
            if isinstance(obj, player) and not obj.destroyed:
                if obj in self.player_one.units:
                    painter().draw_unit(convert, self.canvas, brd, self.symbol_size, convert.convert_map_to_logical(obj.loc), self.player_one.color)
                    
                if obj in self.player_two.units:
                    painter().draw_unit(convert, self.canvas, brd, self.symbol_size, convert.convert_map_to_logical(obj.loc), self.player_two.color)
                    
            if isinstance(obj, tree)and not obj.destroyed:
                painter().draw_tree(convert, self.canvas, self.symbol_size, convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, building) and not obj.destroyed:
                painter().draw_building(convert, self.canvas, self.symbol_size, convert.convert_map_to_logical(obj.loc), obj.color)
                
            if isinstance(obj, enemy) and not obj.destroyed:
                painter().draw_unit(convert, self.canvas, brd, self.symbol_size, convert.convert_map_to_logical(obj.loc), colors.symbol_en_color)
                
            if isinstance(obj, broken_cell):
                painter().draw_broken_cell(convert, self.canvas, self.symbol_size, convert.convert_map_to_logical(obj.loc))

        if self.show_stepped_on_tiles:
            for cl in boardmanager.get_all_cells(brd.board):
                painter().draw_square(convert,self.canvas,convert.convert_map_to_logical(cl.loc),colors.green_color)
        print(brd.board)

    def draw_possible_moves(self, unit, movecolor=colors.symbol_dot_color, attackcolor=colors.symbol_attack_dot_color, inspect=False):
        """
        Draws the step / attack moves that are available to the selected unit.
        """
        for i in control.possible_moves(unit, brd):
            painter().draw_dot(convert, self.canvas,convert.convert_map_to_logical(i),movecolor)
        for i in control.possible_moves(unit, brd, total=True, turns=self.controlling_player.available_actions):
            if not inspect:
                painter().draw_dot(convert, self.canvas,convert.convert_map_to_logical(i) ,colors.range_move_color)
            else: 
                painter().draw_dot(convert, self.canvas,convert.convert_map_to_logical(i) ,colors.green_color)
        for i in control.possible_melee_moves(unit, brd.board, self.controlling_player):
            painter().draw_dot(convert, self.canvas,convert.convert_map_to_logical(i) ,colors.symbol_ranged_attack_dot_color, 3)

        for i in control.possible_ranged_moves(unit, brd.board, self.controlling_player):
            painter().draw_dot(convert, self.canvas,convert.convert_map_to_logical(i) ,attackcolor)
    
    def select_move_click(self, event):
        """
        Allows the user to either move a unit, or select another of their units
        """
        grid_position = [event.x, event.y]
        logical_position = convert.convert_grid_to_logical_position(grid_position)
        mappos = convert.convert_logical_to_map(logical_position)

        def _select_unit_click(event):
            grid_position = [event.x, event.y]
            logical_position = convert.convert_grid_to_logical_position(grid_position)
            mappos = convert.convert_logical_to_map(logical_position)

            if isinstance(brd.inspect(mappos), player) and brd.inspect(mappos) in self.controlling_player.units:
                    self.selected_unit = brd.inspect(mappos)
                    ui.make_unit_card(self.unit_box,self.selected_unit,row=0)
            self.reset(mappos, type="soft")
  
        def _movefunc():
            logical_position = convert.convert_grid_to_logical_position(grid_position)
            mappos = convert.convert_logical_to_map(logical_position)

            self.get_event_info(mappos)
            if hasattr(brd.inspect(mappos), 'walkable'):
                action = control.place(self.selected_unit, mappos, brd)
                if action[1]:
                    brd.board = action[0]
                    self.reset(mappos)
                else: 
                    self.set_impossible_action_text("can't do that")

            self.selected = False
            
        if not self.selected and hasattr(brd.inspect(mappos), 'walkable'):
            self.selected = True
            _movefunc()

        if not self.selected: 
            self.selected = True
            _select_unit_click(event)
        
        else:
            _movefunc()

    def inspect_click(self, event):
        """
        Allows the user to get info about what is on a certain tile.
        """
        grid_position = [event.x, event.y]
        logical_position = convert.convert_grid_to_logical_position(grid_position)
        mappos = convert.convert_logical_to_map(logical_position)
        convert.convert_map_to_logical(mappos)

        un = brd.inspect(mappos)

        def __button_action():
            structure = brd.inspect(mappos)
            if isinstance(structure, building) and not structure.owner:
                self.__capture_click(event)
            if isinstance(structure, building) and structure.owner:
                self.__capture_click(event, "empty")

        if isinstance(un, player) or isinstance(un, enemy):
            self.reset(mappos, type="soft")
            self.draw_possible_moves(un, movecolor=colors.green_color, attackcolor=colors.gray_color, inspect=True)
            modal_popup(self, unit_modal_context("unit description", "unit", un))
        elif isinstance(un, building):
            self.reset(mappos, type="soft")
            self.get_event_info(mappos)
            modal_popup(self, modal_context("capture", "capture_building", __button_action))
        else: 
            self.reset(mappos, type="soft")
            self.get_event_info(mappos)
        return mappos

    def melee_attack_click(self, event):
        """
        Allows the current selected unit to attack objects and other units.
        """
        grid_position = [event.x, event.y]
        logical_position = convert.convert_grid_to_logical_position(grid_position)
        mappos = convert.convert_logical_to_map(logical_position)
        for i in control.possible_melee_moves(self.selected_unit, brd.board, self.controlling_player):
            if i == mappos:
                brd.board = control.attack(mappos, brd.board, self.selected_unit.strength)
                self.reset(mappos)
            else:
                self.set_impossible_action_text('{} has a melee range of {}'.format(self.selected_unit.fullname, self.selected_unit.melee_range))
        return mappos

    def ranged_attack_click(self, event):
        """
        Allows the current selected unit to attack objects and other units.
        """
        grid_position = [event.x, event.y]
        logical_position = convert.convert_grid_to_logical_position(grid_position)
        mappos = convert.convert_logical_to_map(logical_position)
        for i in control.possible_ranged_moves(self.selected_unit, brd.board, self.controlling_player):
            if i == mappos:
                brd.board = control.attack(mappos, brd.board, self.selected_unit.strength)
                self.reset(mappos)
            else:
                self.set_impossible_action_text('{} has a ranged range of {}'.format(self.selected_unit.fullname, self.selected_unit.melee_range))
        return mappos

    def __capture_click(self, event, ctype="normal"):
        """
        Allows the current selected unit to capture buildings.
        """
        grid_position = [event.x, event.y]
        logical_position = convert.convert_grid_to_logical_position(grid_position)
        mappos = convert.convert_logical_to_map(logical_position)
        for i in control.possible_melee_moves(self.selected_unit, brd.board, self.controlling_player):
            if i == mappos:
                structure = brd.inspect(i)
                if isinstance(structure, building) and ctype == "normal":
                    structure.set_color(self.controlling_player.color)
                    self.controlling_player.buildings.append(structure)
                    structure.set_owner(self.controlling_player)
                    self.reset(mappos)
                elif isinstance(structure, building) and ctype == "empty":
                    structure.set_color(colors.symbol_building_color)
                    structure.owner = None 
                    #TODO: Make this remove the buildings from the other owner
                    self.game_controller.other_owner.buildings.pop(structure)
                else:
                    self.set_impossible_action_text('{} can only capture factories.'.format(self.selected_unit.fullname))
            else:
                self.set_impossible_action_text('{} has a capture range of {}'.format(self.selected_unit.fullname, self.selected_unit.melee_range))
        return mappos

    def monitor_state(self):
        """
        Watch the current board status and monitor if a player has lost.
        """
        current_controlling_player = self.controlling_player
        self.controlling_player = self.game_controller.action_or_switch()

        # only force select the a unit of the other player, if the turn is over.
        # also set the action to select and move on player change.
        if current_controlling_player != self.controlling_player:
            self.mode_label['text'] = "Select and move Mode"
            self.canvas.bind('<Button-1>', self.select_move_click)
            self.mode_label['background'] = colors.green_color

            for p, unit in enumerate(self.controlling_player.units):
                if unit.health > 0:
                    self.selected_unit = self.controlling_player.units[p]

        ui.make_player_card(self.player_box, self.controlling_player)
        ui.make_unit_card(self.unit_box,self.selected_unit,row=0)

    def set_impossible_action_text(self, text):
        """
        Lets the user now something is not possible
        """
        self.action_details_label['text'] = text

    def reset(self, mappos, type="hard"):
        """
        Reset the board after an action, reflecting the new state.
        """
        done = self.game_controller.check_game_state()
        if done:
            self.draw_board_and_objects(brd)
            self.display_gameover(done)
            return
        self.set_impossible_action_text("")
        self.get_event_info(mappos)
        if type == "hard":
            self.monitor_state()
        if debug:
            print(brd.show())
        self.canvas.delete("all")
        self.draw_board_and_objects(brd)
        self.draw_possible_moves(self.selected_unit)

    def display_gameover(self, winner: owner):
        """
        Cleans the canvas and shows the winner and score.
        """
        text = 'Winner: {}'.format(winner.name)

        self.canvas.delete("all")
        for widget in self.ui.winfo_children():
            widget.destroy()
        self.ui['background'] = colors.board_background
        self.canvas.unbind('<Button-1>')
        self.statusbar['text'] = ""

        self.canvas.create_text(self.boardsize / 2, self.boardsize / 3, font="cmr 60 bold", fill=winner.color, text=text)
        score_text = 'Results \n'
        self.canvas.create_text(self.boardsize / 2, 5 * self.boardsize / 8, font="cmr 40 bold", fill=colors.green_color,
                                text=score_text)

        score_text = '{} Units Left: '.format(self.game_controller.current_owner.name) + "{}".format(len(self.game_controller.current_owner.units)) + '\n'
        score_text += '{} Units Left: '.format(self.game_controller.other_owner.name) + "{}".format(len(self.game_controller.other_owner.units)) + '\n'

        self.canvas.create_text(self.boardsize / 2, 3 * self.boardsize / 4, font="cmr 30 bold", fill=colors.green_color,
                                text=score_text)
    def save_game(self):
        st.save(brd.board)

    def open_file(self):
        global convert
        gameboard = st.load_file(askopenfilename())
        brd.set_board(gameboard)
        pl1 = owner("player1", colors.symbol_tree_color)
        pl2 = owner("player2", colors.symbol_water_color)
        self.gridsize = 14
        gridsize.set_gridsize(self.gridsize)
        convert = convert_coords(self.gridsize)
        #self.initialise_old_game(pl1, pl2)
        self.home_frame.destroy()

main = game()
main.mainloop()