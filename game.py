
import tkinter as tk
from tkinter.filedialog import askopenfilename

from objectmanager.objects.grid import broken_cell, cell
from objectmanager.objects.scenery import building, water, tree

from gamemanager.settings.settings import debug, gridsize

from conversion.conversion import convert_coords
from gamemanager.board import boardManager
from gamemanager.units import unitController
from saves.state import state

from contexts.settingscontext import settings_context, placement_context
from contexts.uicontext import unit_modal_context, modal_context
from contexts import colorContext
from uibuilder.draw import painter

from uibuilder.ui.screens import initialise_game_screen, display_gameover_screen, finalise_game_screen
from uibuilder.ui.components import make_player_card, make_unit_card, make_admin_card, make_generic_event_card, make_gameevent_card

from uibuilder.ui.home import HomeScreen
from objectmanager.placement.inital import create_pieces
from objectmanager.objects.pawn import pawn

from gamemanager.players.owners import owner
from gamemanager.players.npc import npc
from gamemanager.dm.dm import gameController

brd = boardManager()   
st = state()
game_settings = settings_context()


class game(object):
    """
    Ties the dataframe game backend to a visual frontend.
    """
    def __init__(self, window):
        self.window = window
        self.window.title('GridGame')
        self.window.minsize(width=1400, height=1000)
        self.game_settings = settings_context()
        self.convert = convert_coords(self.game_settings.var_tiles, self.game_settings.var_boardsize)
        self.selected = False
        self.gameDone = False
        self.gameEvents = []

        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar)

        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_game)
        filemenu.add_command(label="Exit")

        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        self.initialise_home(self.game_settings)

    def addEvent(self, event):
        self.gameEvents.insert(0, event)

        # remove the event frame to overcome duplicates with pack
        self.rightcontrolframeevents.destroy()
        make_gameevent_card(self, self.rightcontrolframe)
        make_generic_event_card(self.rightcontrolframeevents, self.gameEvents)
        return self.gameEvents
        
    def playerAction(self):
        """
        - 1 from the available actions for the current player.

        Check if somebody has won the game.
        """

        # if an action results in winning the game
        done = self.game_controller.playerAction("")
        if done[0]:
            self.gameDone = True
            return self.display_gameover(done[1][0])

    def initialise_home(self, settings: settings_context):
        """
        Setup the screen that allows for inputting players.
        """
        return HomeScreen().initialise_home_screen(self, settings, brd, gridsize, self.convert)


    def initialise_game(self, players, settings: settings_context, game_controller: gameController):
        """
        Setup the screen that contains the game board and control.
        """
        self.game_controller = game_controller
        initialise_game_screen(self, players, settings)
        return self.place_initial_board(players, settings)
        
    def place_initial_board(self, players, settings: settings_context):
        """
        Create the pieces based on the game settings, and place them on the board.
        """
        create_pieces(self, players, settings, brd, placement_context('army'))
        self.selected = False
        self.selected_unit = self.game_controller.getCurrentPlayer().units[0]

        make_player_card(self, self.player_box, self.game_controller.getCurrentPlayer(), row=2)
        make_unit_card(self, self.unit_box, self.selected_unit, row=20)
     
        boardDone = finalise_game_screen(self)

        # Game over screen can be tested from here.
        #self.display_gameover(self.game_controller.getCurrentPlayer())

        self.draw_board_and_objects(brd)
        self.draw_possible_movement(self.selected_unit)
        
        # A check to have a npc start moving directly when it is the first player.
        self.npc_player_start()
        return boardDone


    def npc_player_start(self):
        if isinstance(self.game_controller.getCurrentPlayer(), npc):
                self.addEvent("npc is starting")
                self.monitor_state()

    def admin_reset_board(self, event):
        self.game_controller.clearPlayers()

        for i in brd.get_all_objects(brd.board):
            i.remove()
        for i in brd.get_coords_of_all_objects(brd.board):
            brd.board.at[i[0], i[1]] = cell((i[0], i[1]))
        self.place_initial_board(self.game_controller.players, self.game_settings)
        
        return self.draw_board_and_objects(brd)

    def mainloop(self):
        self.window.mainloop()
    
    def end_turn(self):
        self.game_controller.switch_player()

        self.mode_label['text'] = "Select and move Mode"
        self.canvas.bind('<Button-1>', self.select_move_click)
        self.mode_label['background'] = colorContext.green_color

        for p, unit in enumerate(self.game_controller.getCurrentPlayer().units):
            if unit.health > 0:
                self.selected_unit = self.game_controller.getCurrentPlayer().units[p]

        make_player_card(self, self.player_box, self.game_controller.getCurrentPlayer(),row=2)
        make_unit_card(self, self.unit_box,self.selected_unit,row=20)
        self.refresh_board()
        self.draw_possible_movement(self.selected_unit)
        

    def show_stepped_tiles(self):
        """
        Show the tiles that have been walked on.
        """
        if not self.show_stepped_on_tiles:
            self.show_stepped_on_tiles = True
            self.refresh_board()
        else:
            self.show_stepped_on_tiles = False
            self.refresh_board()

    def switch_mode_inspect(self, event):
        """
        Switches the  control mode to inspecting grid elements.
        """
        self.mode_label['text'] = "Inspect Mode"
        self.mode_label['background'] = colorContext.green_color
        self.canvas.bind('<Button-1>', self.inspect_click)

    def switch_mode_selectmove(self, event):
        """
        Switches the  control mode to selecting and moving owned units.
        """
        self.refresh_board()
        self.draw_possible_movement(self.selected_unit)
        self.mode_label['text'] = "Select and move Mode"
        self.mode_label['background'] = colorContext.green_color
        self.canvas.bind('<Button-1>', self.select_move_click)


    def switch_mode_melee_attack(self, event):
        """
        Switches the  control mode to attacking with the selected unit.
        """
        self.refresh_board()
        self.draw_possible_melee_attacks(self.selected_unit)
        
        self.mode_label['text'] = "Melee Attack Mode"
        self.mode_label['background'] = colorContext.red_color
        self.canvas.bind('<Button-1>', self.melee_attack_click)

    def get_event_info(self, event):
        """
        Changes the labels text to reflect the selected unit/cell/action
        """
        self.statusbar['text'] = " Location: {} | Steps: {} | Description: {}".format(event,  unitController.count(self.selected_unit, event),brd.explain(event))

    def draw_board_and_objects(self, boardmanager: boardManager):
        """
        Cleans the board, and draws are elements in the dataframe.
        """
        if self.gameDone:
            return
        def cleanup_func(obj):
            boardmanager.board.at[obj.loc[0], obj.loc[1]] = cell(loc=(obj.loc[0], obj.loc[1]))
            for player in self.players:
                for unit in player.units:
                    if unit == obj:
                        player.units.remove(obj)

        for i in range(self.gridsize):
            self.canvas.create_line((i + 1) * self.game_settings.var_boardsize / self.gridsize, 0, (i + 1) * self.game_settings.var_boardsize / self.gridsize, self.game_settings.var_boardsize)

        for i in range(self.gridsize):
            self.canvas.create_line(0, (i + 1) * self.game_settings.var_boardsize / self.gridsize, self.game_settings.var_boardsize, (i + 1) * self.game_settings.var_boardsize / self.gridsize)
        
        # Changes tiles color after movement slightly
        for obj in boardmanager.get_all_clean_cells(brd.board):
             painter.draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(obj.loc),obj.color)

        for obj in boardmanager.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, water):
                painter.draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(obj.loc),obj.color)
                
            if isinstance(obj, pawn) and not obj.destroyed:
                for i in self.players:
                    if obj in i.units:
                        painter.draw_unit(self.convert, self.canvas, brd, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), i.color)
                    
            if isinstance(obj, tree)and not obj.destroyed:
                painter.draw_tree(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, building) and not obj.destroyed:
                painter.draw_building(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc), obj.color)
                
            if isinstance(obj, broken_cell):
                painter.draw_broken_cell(self.convert, self.canvas, self.symbol_size, self.convert.convert_map_to_logical(obj.loc))

        if self.show_stepped_on_tiles:
            for cl in boardmanager.get_all_used_cells(brd.board):
                painter.draw_square(self.convert,self.canvas,self.convert.convert_map_to_logical(cl.loc),colorContext.green_color)
        if debug:
            print(brd.board)
        
        return True

    def draw_all_possible_moves(self, unit, movecolor=colorContext.symbol_dot_color, attackcolor=colorContext.symbol_attack_dot_color, inspect=False):
        """
        Draws the step / attack moves that are available to the selected unit.
        """
        for i in  unitController.possible_moves(unit, brd):
            painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i),movecolor)

        for i in  unitController.possible_moves(unit, brd, total=True, turns=self.game_controller.getCurrentPlayer().available_actions):
            if not inspect:
                painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colorContext.range_move_color)
            else: 
                painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colorContext.green_color)
        for i in  unitController.possible_melee_moves(unit, brd.board, self.game_controller.getCurrentPlayer()):
            painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,colorContext.symbol_ranged_attack_dot_color, 3)

        for i in  unitController.possible_ranged_moves(unit, brd.board, self.game_controller.getCurrentPlayer()):
            painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,attackcolor)

    def draw_possible_movement(self, unit, inspect=False ):
        col=colorContext.symbol_dot_color
        if inspect:
            col=colorContext.green_color

        for i in  unitController.possible_moves(unit, brd, total=True, turns=self.game_controller.getCurrentPlayer().available_actions):
            painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i),col)

    def draw_possible_melee_attacks(self, unit, inspect=False ):
        """
        Draws the places where an unit can attack (melee)
        """
        col=colorContext.symbol_attack_dot_color
        if inspect:
            col=colorContext.green_color

        for i in  unitController.possible_melee_moves(unit, brd.board, self.game_controller.getCurrentPlayer()):
            painter.draw_dot(self.convert, self.canvas,self.convert.convert_map_to_logical(i) ,col, 3)

    def select_move_click(self, event):
        """
        Allows the user to either move a unit, or select another of their units
        """
        if debug:
            print("select move is called with this event:")
            print(event)
        grid_position = [event.x, event.y]
        logical_position = self.convert.convert_grid_to_logical_position(grid_position)
        mappos = self.convert.convert_logical_to_map(logical_position)

        def _select_unit_click(event):
            grid_position = [event.x, event.y]
            logical_position = self.convert.convert_grid_to_logical_position(grid_position)
            mappos = self.convert.convert_logical_to_map(logical_position)

            if isinstance(brd.inspect(mappos), pawn) and brd.inspect(mappos) in self.game_controller.getCurrentPlayer().units:
                    self.selected_unit = brd.inspect(mappos)
                    make_unit_card(self, self.unit_box,self.selected_unit,row=20)
            self.reset(mappos, type="soft")
  
        def _movefunc():

            logical_position = self.convert.convert_grid_to_logical_position(grid_position)
            mappos = self.convert.convert_logical_to_map(logical_position)
            errorStatus = False
            tmpPos = self.selected_unit.loc

            if isinstance(brd.inspect(mappos), pawn) and brd.inspect(mappos) in self.game_controller.getCurrentPlayer().units:
                errorStatus = False
                self.selected_unit = brd.inspect(mappos)
                self.reset(mappos, type="soft")
            else: 
                errorStatus = True
                    
            self.get_event_info(mappos)
            if hasattr(brd.inspect(mappos), 'walkable'):
                action =  unitController.place(self.selected_unit, mappos, brd)

                if action[1]:
                    errorStatus = False
                    self.playerAction()
                    self.addEvent(f"{self.selected_unit.fullname}: moved from {tmpPos} to {self.selected_unit.loc}")
                    brd.board = action[0]
                    self.reset(mappos)
                else: 
                    # check if it was not a unit switch
                    if self.selected_unit != brd.inspect(mappos):
                        errorStatus = True
                    else:
                        self.set_impossible_action_text(f"{self.game_controller.getCurrentPlayer().name} - selected unit: {self.selected_unit.fullname}")
            
            if errorStatus:
                self.set_impossible_action_text(f"{self.selected_unit.fullname}: can't do that")

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

        if isinstance(un, pawn):
            self.reset(mappos, type="soft")
            self.draw_all_possible_moves(un, movecolor=colorContext.green_color, attackcolor=colorContext.gray_color, inspect=True)
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
        for i in  unitController.possible_melee_moves(self.selected_unit, brd.board, self.game_controller.getCurrentPlayer()):
            if i == mappos:
                self.playerAction()
                brd.board =  unitController.attack(mappos, brd.board, self.selected_unit.strength)
                self.addEvent(f"{self.selected_unit.fullname}: attacked {brd.inspect(mappos)} for {self.selected_unit.strength} DMG ")
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
        for i in  unitController.possible_ranged_moves(self.selected_unit, brd.board, self.game_controller.getCurrentPlayer()):
            if i == mappos:
                self.playerAction()
                brd.board =  unitController.attack(mappos, brd.board, self.selected_unit.strength)
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
        for i in  unitController.possible_melee_moves(self.selected_unit, brd.board, self.game_controller.getCurrentPlayer()):
            if i == mappos:
                structure = brd.inspect(i)
                if isinstance(structure, building) and ctype == "normal":
                    self.playerAction()
                    structure.set_color(self.game_controller.getCurrentPlayer().color)
                    self.game_controller.getCurrentPlayer().buildings.append(structure)
                    structure.set_owner(self.game_controller.getCurrentPlayer())
                    self.reset(mappos)
                elif isinstance(structure, building) and ctype == "empty":
                    self.playerAction()
                    structure.set_color(colorContext.symbol_building_color)
                    structure.owner = None 
                    #TODO: Make this remove the buildings from the other owner
                else:
                    self.set_impossible_action_text('{} can only capture factories.'.format(self.selected_unit.fullname))
            else:
                self.set_impossible_action_text('{} has a capture range of {}'.format(self.selected_unit.fullname, self.selected_unit.melee_range))
        return mappos

    def monitor_state(self):
        """
        Watch the current board status and monitor if a player has lost.
        Also checks if the player is an npc, and if so, calls the its 'makedecision' function.
        """

        self.mode_label['text'] = "Select and move Mode"
        self.canvas.bind('<Button-1>', self.select_move_click)
        self.mode_label['background'] = colorContext.green_color

        if self.selected_unit not in self.game_controller.getCurrentPlayer().units:
            for p, unit in enumerate(self.game_controller.getCurrentPlayer().units):
                if unit.health > 0:
                    self.selected_unit = self.game_controller.getCurrentPlayer().units[p]

        make_player_card(self, self.player_box, self.game_controller.getCurrentPlayer(),row=2)
        make_unit_card(self, self.unit_box,self.selected_unit,row=20)

        # ! IF the current player is an npc, make an decision
        if isinstance( self.game_controller.getCurrentPlayer(), npc):
            self.game_controller.makePlayerDecision(self.selected_unit)
            self.draw_board_and_objects(brd)
        
        return True
            

    def set_impossible_action_text(self, text):
        """
        Lets the user now something is not possible
        """
        ertxt = "Error: " + text
        self.addEvent(ertxt)

    def refresh_board(self):
        """
        Delete all objects on the board, and refresh the windows.
        Then draw them again.
        """
        if not self.gameDone:
            self.canvas.delete("all")
            self.window.update()
            self.draw_board_and_objects(brd)
            self.canvas.update()
            self.canvas.update_idletasks()

    def reset(self, mappos=None, type="hard"):
        """
        Reset the board after an action, reflecting the new state.
        """
        if mappos:
            self.get_event_info(mappos)

        if not self.gameDone:
            self.refresh_board()

        if type == "hard" and not self.gameDone:
            self.monitor_state()
        if debug:
            print(brd.show())
        if not self.gameDone:
            self.draw_possible_movement(self.selected_unit)
        return True

    def display_gameover(self, winner: owner):
        """
        Delete all the objects on the board,
        Display the end game screen that shows the winner.
        """
        #self.canvas.delete("all")
        #self.canvas.update()
        return display_gameover_screen(self, winner)

    def save_game(self):
        st.save(brd.board)

    def open_file(self):
        gameboard = st.load_file(askopenfilename())
        brd.set_board(gameboard)
        self.gridsize = 14
        gridsize.set_gridsize(self.gridsize)
        self.convert = convert_coords(self.gridsize)
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
    root.geometry("1600x1000")
    main.mainloop()