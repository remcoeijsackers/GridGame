import numpy as np
import random
from tkinter import *
import tkinter as tk

from src.manager import manager, unitcontroller, placement
from src.util import placeip, cols, colsandrows, fullcols, colsr, colsc
from src.state import state
from src.objects import broken_cell, player, cell, scenery, unit, building, enemy, water, tree

from src.settings import gridsize, debug, player_one_name, player_two_name, player_one_color, player_two_color
from src.constants import size_of_board, number_of_col_squares, symbol_size, symbol_thickness, unit_thickness
from src.conversion import convert_coords

from src.controller import controller, owner

board_background = '#2e1600'
symbol_X_color = '#EE4035'
symbol_tree_color = 'green'
symbol_dot_color = '#A999CC'
symbol_En_color = '#EE4035'
symbol_attack_dot_color = '#ccc1CF'
Green_color = '#7BC043'
Red_color = '#EE4035'
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

        self.statusbar = tk.Label(self.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, background=board_background)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = Canvas(self.window, bd=1)
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Controls", background='#EE5E51')

        self.turn_label = tk.Label(self.ui, text="{}".format(player_one.name), background=player_one.color)
        self.actions_label = tk.Label(self.ui, text="Actions remaining: 4", background=player_one.color)
        self.placeholder_label = tk.Label(self.ui, text="")

        #self.loc_label = tk.Label(self.ui, text="loc")
        self.info_label = tk.Label(self.ui, text="info")
        self.desc_label = tk.Label(self.ui, text="description")
        self.health_label = tk.Label(self.ui, text="health")
        self.mode_label = tk.Label(self.ui, text="Select and move Mode", background=Green_color)
        #self.distance_label = tk.Label(self.ui, text="Distance")
        self.action_details_label = tk.Label(self.ui, text="Action details")

        self.move_button = tk.Button(self.ui, text="Select move")
        self.inspect_button = tk.Button(self.ui, text="Inspect Cell")
        self.melee_attack_button = tk.Button(self.ui, text="Melee Attack")
    
        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.turn_label.grid(column=0, row=1, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.actions_label.grid(column=0, row=2, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.placeholder_label.grid(column=0, row=3, sticky=tk.EW, columnspan = self.max_ui_columns)

        #self.loc_label.grid(column=0, row=4, sticky=tk.E,padx=5, pady=5)
        self.info_label.grid(column=1, row=4,sticky=tk.W, padx=5, pady=5)
        self.desc_label.grid(column=2, row=4,sticky=tk.E, padx=5, pady=5)
        self.health_label.grid(column=3, row=4,sticky=tk.E, padx=5, pady=5)

        #self.distance_label.grid(column=0, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 2)
        self.action_details_label.grid(column=2, row=5,sticky=tk.W, padx=5, pady=5,columnspan = 3)
        
        self.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.move_button.grid(column=0, row=7, sticky=tk.W, columnspan = 2)
        self.inspect_button.grid(column=1, row=7, sticky=tk.S, columnspan = 2)

        self.melee_attack_button.grid(column=2,sticky=tk.E,  row=7, columnspan = 2)

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
        brd.placeclus(water_clus)
        brd.placeclus(water_clus2)

        self.controlling_player = player_one
        self.selected = False
        self.selected_unit = self.controlling_player.units[0]

        self.draw_board_and_objects(brd)
        self.draw_possible_moves(self.selected_unit)
        #self.display_gameover(self.controlling_player)
        #self.popupmsg("hi")
        self.pop_up()

    def mainloop(self):
        """
        Runs the tkinter application.
        """
        self.window.mainloop()

    def pop_up(self):
    	popUp(self)

    def popupmsg(self, msg):
        popup = Tk()
        popup.wm_title("!")
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()

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
        self.statusbar['text'] = " Location: {} | Steps: {} |".format(event, control.count(self.selected_unit, event))
        self.info_label['text'] = "Unit: {}".format(brd.inspect(event))
        self.desc_label['text'] = "Description: {}".format(brd.explain(event))
        self.health_label['text'] = "Health: {}".format(brd.gethealth(event))
        #self.distance_label['text'] = "Steps: {}".format(control.count(self.selected_unit, event))

    def draw_board_and_objects(self, boardmanager: manager):
        """
        Cleans the board, and draws are elements in the dataframe.
        """
        def cleanup_func(obj):
            boardmanager.board.at[obj.loc[0], obj.loc[1]] = cell()
            if obj in player_one.units:
                player_one.units.remove(obj)
            if obj in player_two.units:
                player_two.units.remove(obj)

        for i in range(number_of_col_squares):
            self.canvas.create_line((i + 1) * size_of_board / number_of_col_squares, 0, (i + 1) * size_of_board / number_of_col_squares, size_of_board)

        for i in range(number_of_col_squares):
            self.canvas.create_line(0, (i + 1) * size_of_board / number_of_col_squares, size_of_board, (i + 1) * size_of_board / number_of_col_squares)

        for obj in boardmanager.get_all_objects(brd.board):
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
        self.controlling_player = game_controller.action_or_switch()

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
        done = game_controller.check_game_state()
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

        score_text = '{} Units Left: '.format(game_controller.current_owner.name) + "{}".format(len(game_controller.current_owner.units)) + '\n'
        score_text += '{} Units Left: '.format(game_controller.other_owner.name) + "{}".format(len(game_controller.other_owner.units)) + '\n'

        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
                
if __name__ == "__main__":
    main = game()
    main.mainloop()