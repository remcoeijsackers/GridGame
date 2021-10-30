import numpy as np
import random
from tkinter import *
import tkinter as tk

from manager import manager, unitcontroller, placement
from util import placeip, cols, colsandrows, fullcols, colsr, colsc
from state import state
from objects import broken_cell, player, cell, scenery, unit, building, enemy

from settings import gridsize, debug

from controller import controller, owner

size_of_board = 600
number_of_col_squares = gridsize
symbol_size = (size_of_board / number_of_col_squares - size_of_board / 8) / 2
symbol_thickness = 40
symbol_X_color = '#EE4035'
symbol_O_color = '#A9CCCC'
symbol_dot_color = '#A999CC'
symbol_Sq_color = '#9363FF'
symbol_Pl_color = '#E0f9FF'
symbol_Pl2_color = '#99f9CF'
symbol_En_color = '#EE4035'
symbol_attack_dot_color = '#ccc1CF'
Green_color = '#7BC043'
symbol_building_color = '#E0f9FF'
black_color = '#120606'
canvas_text_color = '#9363FF'

player_one = owner("Player1")
player_two = owner("Player2")
game_controller = controller(player_one, player_two)

brd = manager()   
st = state()

user = player("P")
user2 = player("P2")

player_one.units.append(user)
player_two.units.append(user2)

foe = enemy("E")
house = building("B")
tree = scenery("T")
tree2 = scenery("T")
tree3 = scenery("T")
tree4 = scenery("T")
control = unitcontroller()
gen = placement(str(random.randint(10000000000, 99999999999)))

placeip(brd.board, user)
placeip(brd.board, user2)
placeip(brd.board, foe)
placeip(brd.board, house)
placeip(brd.board, tree)
placeip(brd.board, tree2)
placeip(brd.board, tree3)
placeip(brd.board, tree4)

# random seed placement
#brd.board = gen.generate(brd.board)

class visual():
    def __init__(self):
        self.window = Tk()
        self.window.title('GridGame')
        self.window.minsize(width=1000, height=600)

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = Canvas(self.window, bd=1, background='#0492CF')
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Controls", background='#EE5E51')
        self.turn_label = tk.Label(self.ui, text="Player 1 is in control")
        self.actions_label = tk.Label(self.ui, text="Actions remaining: 3")
        self.placeholder_label = tk.Label(self.ui, text="")

        self.loc_label = tk.Label(self.ui, text="loc")
        self.info_label = tk.Label(self.ui, text="info")
        self.desc_label = tk.Label(self.ui, text="description")
        self.health_label = tk.Label(self.ui, text="health")
        self.mode_label = tk.Label(self.ui, text="Select and move Mode")
        self.distance_label = tk.Label(self.ui, text="Distance")
        self.action_details_label = tk.Label(self.ui, text="Action details")


        self.move_button = tk.Button(self.ui, text="Move")
        self.click_button = tk.Button(self.ui, text="Interact")
        self.inspect_button = tk.Button(self.ui, text="Inspect")
        self.select_to_move_button = tk.Button(self.ui, text="select and move")
        self.select_unit_button = tk.Button(self.ui, text="select unit to control")
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

        self.click_button.grid(column=0, row=8,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.select_to_move_button.grid(column=0, row=10,sticky=tk.EW, columnspan = self.max_ui_columns)
        self.select_unit_button.grid(column=0, row=11,sticky=tk.EW, columnspan = self.max_ui_columns)
        self.melee_attack_button.grid(column=0, row=12,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.ui.pack(side='right',anchor='nw',expand=True,fill='both')

        self.move_button.bind('<Button-1>', self.switch_mode_move)
        self.click_button.bind('<Button-1>', self.switch_mode_click)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)
        self.select_to_move_button.bind('<Button-1>', self.switch_mode_selectmove)
        self.select_unit_button.bind('<Button-1>', self.switch_mode_select_unit)
        self.melee_attack_button.bind('<Button-1>', self.switch_mode_melee_attack)

        # Input from user in form of clicks
        self.canvas.bind('<Button-1>', self.select_move_click)
        self.controlling_player = player_one
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(number_of_col_squares, number_of_col_squares))
        self.draw_scenery()
        self.selected = False
        self.cached_loc = any
        self.selected_unit = user
        self.draw_possible_moves(self.selected_unit)
        self.draw_possible_melee_attack(self.selected_unit)

        self.reset_board = False
        self.gameover = False

    def mainloop(self):
        self.window.mainloop()
    
    def switch_mode_move(self, event):
        self.mode_label['text'] = "Move Mode"
        self.canvas.bind('<Button-1>', self.moveclick)
    
    def switch_mode_click(self, event):
        self.mode_label['text'] = "Click Mode"
        self.canvas.bind('<Button-1>', self.click)
    
    def switch_mode_inspect(self, event):
        self.mode_label['text'] = "Inspect Mode"
        self.canvas.bind('<Button-1>', self.inspectclick)

    def switch_mode_selectmove(self, event):
        self.mode_label['text'] = "Select and move Mode"
        self.canvas.bind('<Button-1>', self.select_move_click)
    
    def switch_mode_select_unit(self, event):
        self.mode_label['text'] = "Select Unit Mode"
        self.canvas.bind('<Button-1>', self.select_unit_click)
    
    def switch_mode_melee_attack(self, event):
        self.mode_label['text'] = "Melee Attack Mode"
        self.canvas.bind('<Button-1>', self.melee_attack_click)


    def show_loc(self, event):
        self.loc_label['text'] = event
        self.info_label['text'] = brd.inspect(event)
        self.desc_label['text'] = brd.explain(event)
        self.health_label['text'] = brd.gethealth(event)
        self.distance_label['text'] = control.count(self.selected_unit, event)
        #tk.Label(self.ui, text = "{}".format(event)).pack(side="right")

    def initialize_board(self):
        for i in range(number_of_col_squares):
            self.canvas.create_line((i + 1) * size_of_board / number_of_col_squares, 0, (i + 1) * size_of_board / number_of_col_squares, size_of_board)

        for i in range(number_of_col_squares):
            self.canvas.create_line(0, (i + 1) * size_of_board / number_of_col_squares, size_of_board, (i + 1) * size_of_board / number_of_col_squares)


    def draw_scenery(self):
        def cleanup_func(obj):
            brd.board.at[obj.loc[0], obj.loc[1]] = cell()

        for obj in brd.get_all_objects(brd.board):
            if obj.destroyed:
                cleanup_func(obj)
            if isinstance(obj, player) and not obj.destroyed:
                self.draw_unit(self.convert_map_to_logical(obj.loc), symbol_Pl_color)
            if isinstance(obj, scenery)and not obj.destroyed:
                self.draw_O(self.convert_map_to_logical(obj.loc))
            if isinstance(obj, building) and not obj.destroyed:
                self.draw_building(self.convert_map_to_logical(obj.loc))
            if isinstance(obj, enemy) and not obj.destroyed:
                self.draw_unit(self.convert_map_to_logical(obj.loc), symbol_En_color)
            if isinstance(obj, broken_cell):
                self.draw_X(self.convert_map_to_logical(obj.loc))

    def draw_possible_moves(self, unit):
        for i in control.possible_moves(unit, brd):
            #if i not in filter_coords:
                self.draw_dot(self.convert_map_to_logical(i), symbol_dot_color)
            
    def draw_possible_melee_attack(self, unit):
        for i in control.possible_melee_moves(unit, brd.board, self.controlling_player):
            self.draw_dot(self.convert_map_to_logical(i), symbol_attack_dot_color)

    def play_again(self):
        self.initialize_board()
        self.board_status = np.zeros(shape=(number_of_col_squares, number_of_col_squares))

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def draw_Sq(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_Sq_color)
    def draw_building(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_rectangle(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_building_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=black_color)
        self.canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=canvas_text_color, text="hi")

    def draw_unit(self, logical_position, color, owner="", type=""):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        mappos = self.convert_logical_to_map(logical_position)
        health = brd.gethealth(mappos)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=color)
        self.canvas.create_text(grid_position[0] - symbol_size,
                                grid_position[1] + symbol_size, 
                                fill=canvas_text_color, text=health)
    
    def draw_dot(self, logical_position, color):
        width = 10
        if color == symbol_attack_dot_color:
            width = 20
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=width,
                                outline=color)
    
    def clear_cell(self, widget_id):
        self.canvas.delete(widget_id)

    def display_gameover(self, winner: owner):

        self.X_score += 1
        text = 'Winner: {}'.format(winner.name)
        color = symbol_X_color


        self.canvas.delete("all")
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

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / number_of_col_squares) * logical_position + size_of_board / (number_of_col_squares * 2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / number_of_col_squares), dtype=int)

    def convert_logical_to_map(self, logical_postion):
        alp = [i for i in logical_postion]
        letter = colsr.get(alp[0])
        map_position = (alp[1], letter)
        return map_position
        
    def convert_map_to_logical(self, map_position):
        number = colsc.get(map_position[1])
        log_pos = np.array([number, map_position[0]], dtype=int)
        return log_pos
    
    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        self.convert_map_to_logical(mappos)
        self.show_loc(mappos)

        if self.controlling_player == player_one:
            if hasattr(logical_position, 'walkable'):
                self.draw_X(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = -1
                self.player_X_turns = not self.player_X_turns
            else:
                # if position on grid has an icon, return the id
                widget_id = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
                self.clear_cell(widget_id)
                self.board_status[logical_position[0]][logical_position[1]] = 0
                return widget_id
        if self.controlling_player == player_two:
            if hasattr(logical_position, 'walkable'):
                self.draw_O(logical_position)
                self.board_status[logical_position[0]][logical_position[1]] = 1
                self.player_X_turns = not self.player_X_turns
            else:
                # if position on grid has an icon, return the id
                widget_id = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
                self.clear_cell(widget_id)
                self.board_status[logical_position[0]][logical_position[1]] = 0
                return widget_id

        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
        return mappos

    def moveclick(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        self.convert_map_to_logical(mappos)
        action = control.place(self.selected_unit, mappos, brd)
        if action[1]:
            brd.board = action[0]
            self.reset(mappos)
        else:
            self.set_impossible_action_text("cannot move there")
        return mappos

    def select_move_click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)

        def movefunc():
            logical_position = self.convert_grid_to_logical_position(grid_position)
            mappos = self.convert_logical_to_map(logical_position)

            self.show_loc(mappos)
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
            movefunc()

        if not self.selected: 
            self.selected = True
            self.select_unit_click(event)
        
        else:
            movefunc()



    def select_unit_click(self, event):
        global user
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)

        if isinstance(brd.inspect(mappos), player):
            if brd.inspect(mappos) in self.controlling_player.units:
                self.selected_unit = brd.inspect(mappos)
        self.soft_reset(mappos)
        return user


    def inspectclick(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        self.convert_map_to_logical(mappos)

        self.show_loc(mappos)
        return mappos

    def place_on_map(self, map_postion, item):
        logical_position = self.convert_map_to_logical(map_postion)
        self.draw_Sq(logical_position)

    def melee_attack_click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        for i in control.possible_melee_moves(self.selected_unit, brd.board, self.controlling_player):
            if i == mappos:
                brd.board = control.attack(mappos, brd.board, self.selected_unit.strength)
                self.reset(mappos)
            else:
                self.set_impossible_action_text('{} has a melee range of {}'.format(self.selected_unit, self.selected_unit.melee_range))
        return mappos

    def monitor_state(self):
        self.controlling_player = game_controller.action_or_switch()
        self.selected_unit = self.controlling_player.units[0]
        self.turn_label['text'] = self.controlling_player.name
        self.actions_label['text'] = self.controlling_player.available_actions + 1

    def set_impossible_action_text(self, text):
        self.action_details_label['text'] = text

    def reset(self, mappos):
        done = game_controller.check_game_state()
        if done:
            self.canvas.delete("all")
            self.display_gameover(done)
            return
        self.set_impossible_action_text("")
        self.show_loc(mappos)
        self.monitor_state()
        if debug:
            print(brd.show())
        self.canvas.delete("all")
        self.play_again()
        self.draw_scenery()
        self.draw_possible_moves(self.selected_unit)
        self.draw_possible_melee_attack(self.selected_unit)

    def soft_reset(self, mappos):
        done = game_controller.check_game_state()
        if done:
            self.canvas.delete("all")
            self.display_gameover(done)
            return
        self.set_impossible_action_text("")
        self.show_loc(mappos)
        if debug:
            print(brd.show())
        self.canvas.delete("all")
        self.play_again()
        self.draw_scenery()
        self.draw_possible_moves(self.selected_unit)
        self.draw_possible_melee_attack(self.selected_unit)


def get_input():
    action = input("Options:\nmove(up/down/left/right), attack(up/down/left/right).\ninspect(cell), place(cell), his, load(file), exit. \nwhat now?")
    #vis.mainloop()
    def cleaninput(action, ip):
        action = action.replace("{} ".format(ip), "")
        return action

    if "move" in action:
        action = cleaninput(action , "move")
        aclist = action.split(" ")
        step = 1
        if len(aclist) > 1:
            step = int(aclist[1])
        brd.board = control.move(aclist[0], user, brd.board)
        st.save(brd.board)
        control.moverange(user, brd.board)
    
    if "attack" in action:
        action = cleaninput(action , "attack")
        brd.board = control.attack(action, user, brd.board)
        st.save(brd.board)
        if debug:
            print(brd.show())
        #control.moverange(user, brd.board)

    if "place" in action:
        action = cleaninput(action, "place")
        brd.board = control.place(user, action, brd)
        if debug:
            print(brd.show())

    if "inspect" in action:
        action = cleaninput(action, "inspect")
        brd.inspect(action)

    if "his" in action:
        print(st.his)
        print("\n")

    if "load" in action:
        action = cleaninput(action, "load")
        brd.board = st.load(action)
        user.loc = brd.search("P")
        #for item in brd.board:
        #    item.set_loc(brd.search(item.name))
        print(brd.show())
    vis.window.after(0, get_input)

    if "exit" in action:
        vis.window.quit()
        st.close()

vis = visual()
#vis.window.after(0, get_input)
vis.mainloop()