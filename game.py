
import tkinter as tk
from tkinter.filedialog import askopenfilename

from src.manager import manager, unitcontroller
from src.state import state
from src.objects import broken_cell, player, cell, building, enemy, water, tree

from src.settings import debug, gridsize
from src.conversion import convert_coords
from src.controller import  owner
from src.context import modal_context, settings_context, color_context, unit_modal_context, placement_context
from src.ui import painter

from uibuilder.ui.screens import initialise_home_screen, initialise_game_screen, display_gameover_screen, initialise_canvas, finalise_game_screen
from uibuilder.ui.components import make_player_card, make_unit_card, initilise_settings, make_admin_card,make_unit_event_card

from objectmanager.placement.inital import create_pieces

colors = color_context()
brd = manager()   
st = state()
control = unitcontroller()
game_settings = settings_context()

class game(object):
    """
    Ties the dataframe game backend to a visual frontend.
    """
    def __init__(self, window):
        self.window = window
        self.window.title('GridGame')
        self.window.minsize(width=1000, height=600)
        self.itemPlacement = "rigid"
        self.game_settings = settings_context()
        self.convert = convert_coords(self.game_settings.var_tiles, self.game_settings.var_boardsize)

        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar)

        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_game)
        filemenu.add_command(label="Exit")

        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        self.initialise_home(self.game_settings)
        
    def initialise_home(self, settings: settings_context):
        return initialise_home_screen(self, settings, brd, gridsize)

    def initialise_game(self, player_one, player_two, settings: settings_context):
        initialise_game_screen(self, player_one, player_two, settings)
        return self.place_initial_board(player_one,player_two,settings)
        
    def place_initial_board(self, player_one, player_two, settings: settings_context):
        create_pieces(self, player_one,player_two,settings, brd, placement_context('army'))
        self.controlling_player = player_one
        self.selected = False
        self.selected_unit = self.controlling_player.units[0]

        make_player_card(self.player_box, self.controlling_player)
        make_unit_card(self, self.unit_box, self.selected_unit, row=20)
     
        make_admin_card(self, self.admin_box, row=22)

        finalise_game_screen(self)

        self.draw_board_and_objects(brd)
        self.draw_possible_moves(self.selected_unit)

    def admin_reset_board(self, event):
        self.player_one.clear()
        self.player_two.clear()
        for i in brd.get_all_objects(brd.board):
            i.remove()
        for i in brd.get_coords_of_all_objects(brd.board):
            brd.board.at[i[0], i[1]] = cell()
        self.place_initial_board(self.player_one,self.player_two,self.game_settings)
        
        return self.draw_board_and_objects(brd)

    def mainloop(self):
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
            self.canvas.create_line((i + 1) * self.game_settings.var_boardsize / self.gridsize, 0, (i + 1) * self.game_settings.var_boardsize / self.gridsize, self.game_settings.var_boardsize)

        for i in range(self.gridsize):
            self.canvas.create_line(0, (i + 1) * self.game_settings.var_boardsize / self.gridsize, self.game_settings.var_boardsize, (i + 1) * self.game_settings.var_boardsize / self.gridsize)
        
        # Changes tiles color after movement slightly
        for obj in boardmanager.get_all_clean_cells(brd.board):
            painter().draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(obj.loc),obj.color)

        for obj in boardmanager.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, water):
                painter().draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(obj.loc),obj.color)
                
            if isinstance(obj, player) and not obj.destroyed:
                if obj in self.player_one.units:
                    painter().draw_unit(self.convert, self.canvas, brd, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), self.player_one.color)
                    
                if obj in self.player_two.units:
                    painter().draw_unit(self.convert, self.canvas, brd, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), self.player_two.color)
                    
            if isinstance(obj, tree)and not obj.destroyed:
                painter().draw_tree(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, building) and not obj.destroyed:
                painter().draw_building(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), obj.color)
                
            if isinstance(obj, enemy) and not obj.destroyed:
                painter().draw_unit(self.convert, self.canvas, brd, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), colors.symbol_en_color)
                
            if isinstance(obj, broken_cell):
                painter().draw_broken_cell(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc))

        if self.show_stepped_on_tiles:
            for cl in boardmanager.get_all_cells(brd.board):
                painter().draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(cl.loc),colors.green_color)
        print(brd.board)

    def draw_possible_moves(self, unit, movecolor=colors.symbol_dot_color, attackcolor=colors.symbol_attack_dot_color, inspect=False):
        """
        Draws the step / attack moves that are available to the selected unit.
        """
        for i in control.possible_moves(unit, brd):
            painter().draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i),movecolor)
        for i in control.possible_moves(unit, brd, total=True, turns=self.controlling_player.available_actions):
            if not inspect:
                painter().draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colors.range_move_color)
            else: 
                painter().draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colors.green_color)
        for i in control.possible_melee_moves(unit, brd.board, self.controlling_player):
            painter().draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colors.symbol_ranged_attack_dot_color, 3)

        for i in control.possible_ranged_moves(unit, brd.board, self.controlling_player):
            painter().draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,attackcolor)
    
    def select_move_click(self, event):
        """
        Allows the user to either move a unit, or select another of their units
        """
        grid_position = [event.x, event.y]
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)

        def _select_unit_click(event):
            grid_position = [event.x, event.y]
            logical_position = self.convert.convert_grid_to_logical_position(grid_position)
            mappos = self.convert.convert_logical_to_map(logical_position)

            if isinstance(brd.inspect(mappos), player) and brd.inspect(mappos) in self.controlling_player.units:
                    self.selected_unit = brd.inspect(mappos)
                    make_unit_card(self, self.unit_box,self.selected_unit,row=20)
            self.reset(mappos, type="soft")
  
        def _movefunc():
            logical_position = self.convert.convert_grid_to_logical_position(grid_position)
            mappos = self.convert.convert_logical_to_map(logical_position)

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

    def test_modal(self, event):

        toplevel = tk.Toplevel()
        label1 = tk.Label(toplevel, text="ABOUT_TEXT", height=0, width=100)
        label1.pack()
        label2 = tk.Label(toplevel, text="DISCLAIMER", height=0, width=100)
        label2.pack()


    def inspect_click(self, event):
        """
        Allows the user to get info about what is on a certain tile.
        """
        grid_position = [event.x, event.y]
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)
        self.convert.convert_map_to_logical(mappos)

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
            self.window.withdraw()
            modal_popup(self, unit_modal_context("unit description", "unit", un))
        elif isinstance(un, building):
            self.reset(mappos, type="soft")
            self.get_event_info(mappos)
            self.window.withdraw()
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
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)
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
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)
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
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)
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
                    #self.game_controller.other_owner.buildings.pop(structure)
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

        make_player_card(self.player_box, self.controlling_player)
        make_unit_card(self, self.unit_box,self.selected_unit,row=20)

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
        return display_gameover_screen(self, winner)

    def save_game(self):
        st.save(brd.board)

    def open_file(self):
        gameboard = st.load_file(askopenfilename())
        brd.set_board(gameboard)
        pl1 = owner("player1", colors.symbol_tree_color)
        pl2 = owner("player2", colors.symbol_water_color)
        self.gridsize = 14
        gridsize.set_gridsize(self.gridsize)
        self.convert = convert_coords(self.gridsize)
        #self.initialise_old_game(pl1, pl2)
        self.home_frame.destroy()

class modal_popup(tk.Toplevel):

    def __init__(self, original, context: modal_context):

        self.original_frame = original
        tk.Toplevel.__init__(self)

        self.transient(root)
        self.geometry("260x210")
        self.lift()

        title = tk.Label(self, text = context.title)
        title.grid(row=0, column=0, sticky=tk.EW)

        if context.ctype == "unit":
            make_unit_card(original, self, context.unit, row=0)

        if context.command:
            context_btn = tk.Button(self, text=context.ctype, command=context.command)
            context_btn.grid(row=3, column=0)
        btn = tk.Button(self, text ="Close", command= lambda : self.on_close())
        btn.grid(row =1)
    def on_close(self):
        self.destroy()
        self.original_frame.window.update()
        self.original_frame.window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    main = game(root)
    root.geometry("1400x1000")
    main.mainloop()