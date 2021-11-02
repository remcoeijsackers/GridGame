import numpy as np
import random
from tkinter import *
import tkinter as tk
from tkinter.colorchooser import askcolor

from src.manager import manager, unitcontroller, placement
from src.util import placeip, cols, colsandrows, fullcols, colsr, colsc
from src.state import state
from src.objects import broken_cell, player, cell, scenery, unit, building, enemy, water, tree

from src.settings import gridsize, debug
from src.constants import size_of_board, symbol_size, symbol_thickness, unit_thickness
from src.conversion import convert_coords

from src.controller import controller, owner

board_background = '#2e1600'
symbol_X_color = '#EE4035'
symbol_tree_color = 'green'
symbol_dot_color = '#A999CC'
symbol_En_color = '#EE4035'
symbol_attack_dot_color = '#EE4035'
Green_color = '#7BC043'
Red_color = '#EE4035'
symbol_building_color = '#E0f9FF'
symbol_water_color = 'blue'
black_color = '#120606'
canvas_text_color = '#9363FF'

brd = manager()   
st = state()
control = unitcontroller()
convert = any

gen = placement(str(random.randint(10000000000, 99999999999)))

# random seed placement
#brd.board = gen.generate(brd.board)

class popUp(tk.Toplevel):

    def __init__(self, original):

        self.original_frame = original
        tk.Toplevel.__init__(self)
        self.transient(self.original_frame.window)
        self.geometry("260x210")
        self.lift()
        label = tk.Label(self, text = "This is Popup window")
        label.grid()
        btn = tk.Button(self, text ="Close", command= lambda : self.on_close())
        btn.grid(row =1)

    def on_close(self):
    	self.destroy()
    	self.original_frame.window.update()
    	self.original_frame.window.deiconify()

class game():
    """
    Ties the dataframe game backend to a visual frontend.
    """
    def __init__(self):
        self.window = Tk()
        self.window.title('GridGame')
        self.window.minsize(width=1000, height=600)

        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Exit")

        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        self.home_frame = tk.Frame(self.window, background=board_background, padx= 10, pady=10)

        entry_player_one = tk.Entry(self.home_frame)
        entry_player_one.insert(0, 'player one')

        entry_player_two = tk.Entry(self.home_frame)
        entry_player_two.insert(0, 'player two')
        entry_player_one['background'] = 'blue'

        tiles = Scale(self.home_frame, from_=10, to=14, orient=HORIZONTAL)


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
            self.gridsize = tiles.get()
            convert = convert_coords(self.gridsize)
            self.initialise_game(pl1,pl2)
            self.home_frame.destroy()

        b0 = tk.Button(
            self.home_frame,
            text='Select a Color for p1',
            command=change_color_p1)
        b1 = tk.Button(
            self.home_frame,
            text='Select a Color for p2',
            command=change_color_p2)

        b2 = tk.Button(self.home_frame, text="Start Game", command=start_game)

        entry_player_one.pack()
        entry_player_two.pack()
        b0.pack(expand=True)
        b1.pack(expand=True)
        tiles.pack()
        b2.pack()
        self.home_frame.pack()
        
    
    def initialise_game(self, player_one, player_two):

        self.player_one = player_one
        self.player_two = player_two
        self.show_stepped_on_tiles = False

        self.game_controller = controller(player_one, player_two)

        self.statusbar = tk.Label(self.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, background=board_background)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = Canvas(self.window, bd=1)
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Controls", background='#EE5E51')

        self.turn_label = tk.Label(self.ui, text="{}".format(self.player_one.name), background=self.player_one.color)
        self.actions_label = tk.Label(self.ui, text="Actions remaining: 4", background=self.player_one.color)
        self.placeholder_label = tk.Label(self.ui, text="")

        #self.loc_label = tk.Label(self.ui, text="loc")
        self.info_label = tk.Label(self.ui, text="info")
        #self.desc_label = tk.Label(self.ui, text="description")
        self.health_label = tk.Label(self.ui, text="health")
        self.mode_label = tk.Label(self.ui, text="Select and move Mode", background=Green_color)
        #self.distance_label = tk.Label(self.ui, text="Distance")
        self.action_details_label = tk.Label(self.ui, text="Action details")

        self.move_button = tk.Button(self.ui, text="Select move")
        self.inspect_button = tk.Button(self.ui, text="Inspect Cell")
        self.melee_attack_button = tk.Button(self.ui, text="Melee Attack")
        self.show_stepped_tiles_button = tk.Button(self.ui, text="show stepped tiles", command=self.show_stepped_tiles)
    
        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.turn_label.grid(column=0, row=1, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.actions_label.grid(column=0, row=2, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.placeholder_label.grid(column=0, row=3, sticky=tk.EW, columnspan = self.max_ui_columns)

        #self.loc_label.grid(column=0, row=4, sticky=tk.E,padx=5, pady=5)
        self.info_label.grid(column=1, row=4,sticky=tk.W, padx=5, pady=5)
        #self.desc_label.grid(column=2, row=4,sticky=tk.E, padx=5, pady=5)
        self.health_label.grid(column=2, row=4,sticky=tk.N, padx=5, pady=5)

        #self.distance_label.grid(column=0, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 2)
        self.action_details_label.grid(column=2, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 3)
        
        self.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.move_button.grid(column=0, row=7, sticky=tk.W, columnspan = 2)
        self.inspect_button.grid(column=1, row=7, sticky=tk.S, columnspan = 2)

        self.melee_attack_button.grid(column=2,sticky=tk.E,  row=7, columnspan = 2)
        self.show_stepped_tiles_button.grid(column=0,sticky=tk.EW,  row=8, columnspan = self.max_ui_columns)
        self.ui.pack(side='right',anchor='nw',expand=True,fill='both')

        self.move_button.bind('<Button-1>', self.switch_mode_selectmove)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)
        self.melee_attack_button.bind('<Button-1>', self.switch_mode_melee_attack)

        self.canvas.bind('<Button-1>', self.select_move_click)

        user,user2 = player("P"), player("P2")
        user3,user4 = player("P3"),player("P4") 

        self.player_one.units.append(user)
        self.player_one.units.append(user2)
        self.player_two.units.append(user3)
        self.player_two.units.append(user4)

        foe = enemy("E")
        house, house2 = building("B"),building("B")
        tree1, tree2, tree3, tree4 = tree("T"),tree("T"),tree("T"),tree("T")
        water_clus, water_clus2 = water("W"),water("W")

        things = [user, user2, user3, user4, foe, house, house2, tree1,tree2,tree3,tree4]
        for i in things:
            placeip(brd.board, i)
        brd.placeclus(water_clus)
        brd.placeclus(water_clus2)

        self.controlling_player = self.player_one
        self.selected = False
        self.selected_unit = self.controlling_player.units[0]

        self.draw_board_and_objects(brd)
        self.draw_possible_moves(self.selected_unit)
        #self.display_gameover(self.controlling_player)
        #self.popupmsg("hi")
        #self.pop_up()

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

    def pop_up(self):
    	popUp(self)

    def switch_mode_inspect(self, event):
        """
        Switches the control mode to inspecting grid elements.
        """
        self.mode_label['text'] = "Inspect Mode"
        self.mode_label['background'] = Green_color
        self.canvas.bind('<Button-1>', self.inspect_click)

    def switch_mode_selectmove(self, event):
        """
        Switches the control mode to selecting and moving owned units.
        """
        self.mode_label['text'] = "Select and move Mode"
        self.mode_label['background'] = Green_color
        self.canvas.bind('<Button-1>', self.select_move_click)
    
    def switch_mode_melee_attack(self, event):
        """
        Switches the control mode to attacking with the selected unit.
        """
        self.mode_label['text'] = "Melee Attack Mode"
        self.mode_label['background'] = Red_color
        self.canvas.bind('<Button-1>', self.melee_attack_click)

    def get_event_info(self, event):
        """
        Changes the labels text to reflect the selected unit/cell/action
        """
        #self.loc_label['text'] = "Location: {}".format(event)
        self.statusbar['text'] = " Location: {} | Steps: {} | Description: {}".format(event, control.count(self.selected_unit, event),brd.explain(event))
        self.info_label['text'] = "Unit: {}".format(brd.inspect(event))
        #self.desc_label['text'] = "Description: {}".format(brd.explain(event))
        self.health_label['text'] = "Health: {}".format(brd.gethealth(event))
        #self.distance_label['text'] = "Steps: {}".format(control.count(self.selected_unit, event))

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
            self.canvas.create_line((i + 1) * size_of_board / self.gridsize, 0, (i + 1) * size_of_board / self.gridsize, size_of_board)

        for i in range(self.gridsize):
            self.canvas.create_line(0, (i + 1) * size_of_board / self.gridsize, size_of_board, (i + 1) * size_of_board / self.gridsize)

        for obj in boardmanager.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, water):
                self.draw_square(convert.convert_map_to_logical(obj.loc), symbol_water_color)
                
            if isinstance(obj, player) and not obj.destroyed:
                if obj in self.player_one.units:
                    self.draw_unit(convert.convert_map_to_logical(obj.loc), self.player_one.color)
                    
                if obj in self.player_two.units:
                    self.draw_unit(convert.convert_map_to_logical(obj.loc), self.player_two.color)
                    
            if isinstance(obj, tree)and not obj.destroyed:
                self.draw_tree(convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, building) and not obj.destroyed:
                self.draw_building(convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, enemy) and not obj.destroyed:
                self.draw_unit(convert.convert_map_to_logical(obj.loc), symbol_En_color)
                
            if isinstance(obj, broken_cell):
                self.draw_broken_cell(convert.convert_map_to_logical(obj.loc))

        if self.show_stepped_on_tiles:
            for cl in boardmanager.get_all_cells(brd.board):
                self.draw_square(convert.convert_map_to_logical(cl.loc), Green_color)
        

                
    def draw_possible_moves(self, unit):
        """
        Draws the step / attack moves that are available to the selected unit.
        """
        for i in control.possible_moves(unit, brd):
            self.draw_dot(convert.convert_map_to_logical(i), symbol_dot_color)
        for i in control.possible_melee_moves(unit, brd.board, self.controlling_player):
            self.draw_dot(convert.convert_map_to_logical(i), symbol_attack_dot_color)
            
    def draw_tree(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness -10,
                                outline=symbol_tree_color)

    def draw_broken_cell(self, logical_position):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def draw_building(self, logical_position):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_rectangle(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1], width=symbol_thickness,
                                fill=symbol_building_color, outline=symbol_building_color)
        self.canvas.create_line(grid_position[0], grid_position[1],
                                grid_position[0], grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=black_color)
        self.canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=canvas_text_color, text="Factory")

    def draw_square(self, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_rectangle(grid_position[0] , grid_position[1],
                                grid_position[0], grid_position[1], width=40,
                                fill=color, outline=color)

    def draw_unit(self, logical_position, color):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        mappos = convert.convert_logical_to_map(logical_position)
        health = brd.gethealth(mappos)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=unit_thickness,
                                fill=color)
        self.canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=canvas_text_color, text=health)
    
    def draw_dot(self, logical_position, color):
        width = 10
        if color == symbol_attack_dot_color:
            width = 20
        if color == Green_color:
            width = 40
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=width,
                                outline=color)

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
                self.set_impossible_action_text('{} has a melee range of {}'.format(self.selected_unit, self.selected_unit.melee_range))
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
            self.mode_label['background'] = Green_color
            self.selected_unit = self.controlling_player.units[0]

        self.turn_label['text'] = self.controlling_player.name
        self.turn_label['background'] = self.controlling_player.color
        self.actions_label['text'] = "Actions remaining: {}".format(self.controlling_player.available_actions + 1)
        self.actions_label['background'] = self.controlling_player.color

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
        self.ui['background'] = board_background
        self.canvas.unbind('<Button-1>')
        self.statusbar['text'] = ""

        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=winner.color, text=text)
        score_text = 'Results \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = '{} Units Left: '.format(self.game_controller.current_owner.name) + "{}".format(len(self.game_controller.current_owner.units)) + '\n'
        score_text += '{} Units Left: '.format(self.game_controller.other_owner.name) + "{}".format(len(self.game_controller.other_owner.units)) + '\n'

        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
                
if __name__ == "__main__":
    main = game()
    main.mainloop()