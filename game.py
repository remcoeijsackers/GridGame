import numpy as np
import random
from tkinter import *
import tkinter as tk

from manager import manager, unitcontroller, placement
from util import placeip, cols, colsandrows, fullcols, colsr, colsc
from state import state
from objects import broken_cell, player, cell, scenery, unit, building, enemy, water, tree

from settings import gridsize, debug, player_one_name, player_two_name, player_one_color, player_two_color
from constants import size_of_board, number_of_col_squares, symbol_size, symbol_thickness, unit_thickness
from conversion import convert_coords

from controller import controller, owner

symbol_X_color = '#EE4035'
symbol_tree_color = 'green'
symbol_dot_color = '#A999CC'
symbol_En_color = '#EE4035'
symbol_attack_dot_color = '#ccc1CF'
Green_color = '#7BC043'
symbol_building_color = '#E0f9FF'
symbol_water_color = 'blue'
black_color = '#120606'
canvas_text_color = '#9363FF'

player_one = owner(player_one_name, player_one_color)
player_two = owner(player_two_name, player_two_color)
game_controller = controller(player_one, player_two)

brd = manager()   
st = state()
control = unitcontroller()
convert = convert_coords()

gen = placement(str(random.randint(10000000000, 99999999999)))

# random seed placement
#brd.board = gen.generate(brd.board)

class game():
    """
    Ties the pandas game backend to a visual frontend.
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

        statusbar = tk.Label(self.window, text="on the way…", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, background='#2e1600')
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = Canvas(self.window, bd=1)
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Controls", background='#EE5E51')
        self.turn_label = tk.Label(self.ui, text="{}".format(player_one.name), background=player_one.color)
        self.actions_label = tk.Label(self.ui, text="Actions remaining: 3")
        self.placeholder_label = tk.Label(self.ui, text="")

        self.loc_label = tk.Label(self.ui, text="loc")
        self.info_label = tk.Label(self.ui, text="info")
        self.desc_label = tk.Label(self.ui, text="description")
        self.health_label = tk.Label(self.ui, text="health")
        self.mode_label = tk.Label(self.ui, text="Select and move Mode")
        self.distance_label = tk.Label(self.ui, text="Distance")
        self.action_details_label = tk.Label(self.ui, text="Action details")

        self.move_button = tk.Button(self.ui, text="Select and move")
        self.inspect_button = tk.Button(self.ui, text="Inspect")
        self.melee_attack_button = tk.Button(self.ui, text="Melee Attack")
    
        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.turn_label.grid(column=0, row=1, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.actions_label.grid(column=0, row=2, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.placeholder_label.grid(column=0, row=3, sticky=tk.EW, columnspan = self.max_ui_columns)

        self.loc_label.grid(column=0, row=4, sticky=tk.E,padx=5, pady=5)
        self.info_label.grid(column=1, row=4,sticky=tk.W, padx=5, pady=5)
        self.desc_label.grid(column=2, row=4,sticky=tk.E, padx=5, pady=5)
        self.health_label.grid(column=3, row=4,sticky=tk.E, padx=5, pady=5)

        self.distance_label.grid(column=0, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 2)
        self.action_details_label.grid(column=2, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 3)
        
        self.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.move_button.grid(column=0, row=7,sticky=tk.W, columnspan = 3)
        self.inspect_button.grid(column=0, row=7,sticky=tk.E, columnspan = 3)

        self.melee_attack_button.grid(column=0, row=12,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.ui.pack(side='right',anchor='nw',expand=True,fill='both')

        self.move_button.bind('<Button-1>', self.switch_mode_selectmove)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)
        self.melee_attack_button.bind('<Button-1>', self.switch_mode_melee_attack)

        self.canvas.bind('<Button-1>', self.select_move_click)

        user,user2 = player("P"), player("P2")
        user3,user4 = player("P3"),player("P4") 

        player_one.units.append(user)
        player_one.units.append(user2)
        player_two.units.append(user3)
        player_two.units.append(user4)

        foe = enemy("E")
        house, house2 = building("B"),building("B")
        tree1, tree2, tree3, tree4 = tree("T"),tree("T"),tree("T"),tree("T")
        water_clus, water_clus2 = water("W"),water("W")

        things = [user, user2, user3, user4, foe, house, house2, tree1,tree2,tree3,tree4]
        for i in things:
            placeip(brd.board, i)
        brd.placeclus(brd, water_clus)
        brd.placeclus(brd, water_clus2)

        self.controlling_player = player_one
        self.selected = False
        self.selected_unit = self.controlling_player.units[0]

        self.draw_board_and_objects()
        self.draw_possible_moves(self.selected_unit)

    def mainloop(self):
        self.window.mainloop()
            
    def switch_mode_inspect(self, event):
        self.mode_label['text'] = "Inspect Mode"
        self.canvas.bind('<Button-1>', self.inspect_click)

    def switch_mode_selectmove(self, event):
        self.mode_label['text'] = "Select and move Mode"
        self.canvas.bind('<Button-1>', self.select_move_click)
    
    def switch_mode_melee_attack(self, event):
        self.mode_label['text'] = "Melee Attack Mode"
        self.canvas.bind('<Button-1>', self.melee_attack_click)

    def get_event_info(self, event):
        self.loc_label['text'] = "Location: {}".format(event)
        self.info_label['text'] = "Unit: {}".format(brd.inspect(event))
        self.desc_label['text'] = "Description: {}".format(brd.explain(event))
        self.health_label['text'] = "Health: {}".format(brd.gethealth(event))
        self.distance_label['text'] = "Steps: {}".format(control.count(self.selected_unit, event))

    def draw_board_and_objects(self):
        def cleanup_func(obj):
            brd.board.at[obj.loc[0], obj.loc[1]] = cell()
            if obj in player_one.units:
                player_one.units.remove(obj)
            if obj in player_two.units:
                player_two.units.remove(obj)

        for i in range(number_of_col_squares):
            self.canvas.create_line((i + 1) * size_of_board / number_of_col_squares, 0, (i + 1) * size_of_board / number_of_col_squares, size_of_board)

        for i in range(number_of_col_squares):
            self.canvas.create_line(0, (i + 1) * size_of_board / number_of_col_squares, size_of_board, (i + 1) * size_of_board / number_of_col_squares)

        for obj in brd.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, water):
                self.draw_water(convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, player) and not obj.destroyed:
                if obj in player_one.units:
                    self.draw_unit(convert.convert_map_to_logical(obj.loc), player_one.color)
                    
                if obj in player_two.units:
                    self.draw_unit(convert.convert_map_to_logical(obj.loc), player_two.color)
                    
            if isinstance(obj, tree)and not obj.destroyed:
                self.draw_tree(convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, building) and not obj.destroyed:
                self.draw_building(convert.convert_map_to_logical(obj.loc))
                
            if isinstance(obj, enemy) and not obj.destroyed:
                self.draw_unit(convert.convert_map_to_logical(obj.loc), symbol_En_color)
                
            if isinstance(obj, broken_cell):
                self.draw_broken_cell(convert.convert_map_to_logical(obj.loc))
                
    def draw_possible_moves(self, unit):
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

    def draw_water(self, logical_position):
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_rectangle(grid_position[0] , grid_position[1],
                                grid_position[0], grid_position[1], width=40,
                                fill=symbol_water_color, outline=symbol_water_color)

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
        logical_position = np.array(logical_position)
        grid_position = convert.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=width,
                                outline=color)
    
    def clear_cell(self, widget_id):
        self.canvas.delete(widget_id)
    
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
            self.soft_reset(mappos)
  
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
        self.convert_map_to_logical(mappos)

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
        self.controlling_player = game_controller.action_or_switch()

        # only force select the a unit of the other player, if the turn is over.
        # also set the action to select and move 
        if current_controlling_player != self.controlling_player:
            self.mode_label['text'] = "Select and move Mode"
            self.canvas.bind('<Button-1>', self.select_move_click)
            self.selected_unit = self.controlling_player.units[0]

        self.turn_label['text'] = self.controlling_player.name
        self.turn_label['background'] = self.controlling_player.color
        self.actions_label['text'] = self.controlling_player.available_actions + 1

    def set_impossible_action_text(self, text):
        """
        Let's the user now something is not possible
        """
        self.action_details_label['text'] = text

    def reset(self, mappos):
        """
        Reset the board after an action, reflecting the new state
        """
        done = game_controller.check_game_state()
        if done:
            self.canvas.delete("all")
            self.display_gameover(done)
            return
        self.set_impossible_action_text("")
        self.get_event_info(mappos)
        self.monitor_state()
        if debug:
            print(brd.show())
        self.canvas.delete("all")
        self.draw_board_and_objects()
        self.draw_possible_moves(self.selected_unit)

    def soft_reset(self, mappos):
        """
        To be able to reset the board, without counting an action
        """
        done = game_controller.check_game_state()
        if done:
            self.canvas.delete("all")
            self.display_gameover(done)
            return
        self.set_impossible_action_text("")
        self.get_event_info(mappos)
        if debug:
            print(brd.show())
        self.canvas.delete("all")
        self.draw_board_and_objects()
        self.draw_possible_moves(self.selected_unit)

    def display_gameover(self, winner: owner):
        """
        Cleans the canvas and shows the winner and score
        """
        text = 'Winner: {}'.format(winner.name)
        color = symbol_X_color

        self.canvas.delete("all")
        self.ui.delete("all")

        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)
        score_text = 'Results \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = '{}: '.format(game_controller.current_owner.name) + "placeholder" + '\n'
        score_text += '{}: '.format(game_controller.other_owner.name) + "placeholder" + '\n'

        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)
                
if __name__ == "__main__":
    main = game()
    main.mainloop()