import numpy as np
import random
from tkinter import *
import tkinter as tk

from manager import manager, unitcontroller, placement
from util import placeip, cols, colsandrows, fullcols, colsr, colsc
from state import state
from objects import player, cell, scenery, unit, building, enemy

from settings import gridsize


size_of_board = 600
number_of_col_squares = gridsize
symbol_size = (size_of_board / number_of_col_squares - size_of_board / 8) / 2
symbol_thickness = 40
symbol_X_color = '#EE4035'
symbol_O_color = '#A9CCCC'
symbol_dot_color = '#A999CC'
symbol_Sq_color = '#9363FF'
symbol_Pl_color = '#E0f9FF'
symbol_En_color = '#EE4035'
Green_color = '#7BC043'

brd = manager()   
st = state()

user = player("P")
foe = enemy("E")
house = building("B")
tree = scenery("T")
tree2 = scenery("T")
tree3 = scenery("T")
tree4 = scenery("T")
control = unitcontroller()
gen = placement(str(random.randint(10000000000, 99999999999)))

placeip(brd.board, user)
placeip(brd.board, foe)
placeip(brd.board, house)
placeip(brd.board, tree)
placeip(brd.board, tree2)
placeip(brd.board, tree3)
placeip(brd.board, tree4)

# random seed placement
#brd.board = gen.generate(brd.board)

control.moverange(user, brd.board)

class visual():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('GridGame')
        self.window.minsize(width=1000, height=600)

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = Canvas(self.window, bd=1, background='#0492CF')
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        
        self.header_label = tk.Label(self.ui, text="Game Options", background='#EE5E51')

        self.loc_label = tk.Label(self.ui, text="loc")
        self.info_label = tk.Label(self.ui, text="info")
        self.desc_label = tk.Label(self.ui, text="description")
        self.move_button = tk.Button(self.ui, text="Move")
        self.click_button = tk.Button(self.ui, text="Interact")
        self.inspect_button = tk.Button(self.ui, text="Inspect")
    
        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = 4)
        self.loc_label.grid(column=0, row=1, sticky=tk.E,padx=5, pady=5)
        self.info_label.grid(column=1, row=1,sticky=tk.W, padx=5, pady=5)
        self.desc_label.grid(column=2, row=1,sticky=tk.E, padx=5, pady=5)
        self.move_button.grid(column=0, row=2,sticky=tk.EW, columnspan = 4)
        self.click_button.grid(column=0, row=3,sticky=tk.EW, columnspan = 4)
        self.inspect_button.grid(column=0, row=4,sticky=tk.EW, columnspan = 4)

        self.ui.pack(side='right',anchor='nw',expand=True,fill='both')

        self.move_button.bind('<Button-1>', self.switch_mode_move)
        self.click_button.bind('<Button-1>', self.switch_mode_click)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)

        # Input from user in form of clicks
        self.canvas.bind('<Button-1>', self.moveclick)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(number_of_col_squares, number_of_col_squares))
        self.draw_scenery()
        self.draw_possible_moves()

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()
    
    def switch_mode_move(self, event):
        print("moveclick")
        #self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', self.moveclick)
    
    def switch_mode_click(self, event):
        #self.canvas.unbind('<Button-1>')
        self.canvas.bind('<Button-1>', self.click)
    
    def switch_mode_inspect(self, event):
        self.canvas.bind('<Button-1>', self.inspectclick)

    def show_loc(self, event):
        self.loc_label['text'] = event
        self.info_label['text'] = brd.inspect(event)
        self.desc_label['text'] = brd.explain(event)
        #tk.Label(self.ui, text = "{}".format(event)).pack(side="right")

    def initialize_board(self):
        for i in range(number_of_col_squares):
            self.canvas.create_line((i + 1) * size_of_board / number_of_col_squares, 0, (i + 1) * size_of_board / number_of_col_squares, size_of_board)

        for i in range(number_of_col_squares):
            self.canvas.create_line(0, (i + 1) * size_of_board / number_of_col_squares, size_of_board, (i + 1) * size_of_board / number_of_col_squares)

        # ui
        #w2 = tk.Label(self.window, 
        #      padx = 10, 
        #      text="hello")
        #w2.pack(side=RIGHT)

    def draw_scenery(self):
        user_pos = self.convert_map_to_logical(user.loc)
        enemy_pos = self.convert_map_to_logical(foe.loc)
        house_pos = self.convert_map_to_logical(house.loc)
        tree_pos = self.convert_map_to_logical(tree.loc)
        tree2_pos = self.convert_map_to_logical(tree2.loc)
        tree3_pos = self.convert_map_to_logical(tree3.loc)
        tree4_pos = self.convert_map_to_logical(tree4.loc)
        things = [user_pos, enemy_pos, house_pos,tree_pos, tree2_pos ,tree3_pos, tree4_pos]

        self.draw_Pl(user_pos)
        self.draw_En(enemy_pos)
        self.draw_Sq(house_pos)
        self.draw_O(tree_pos)
        self.draw_O(tree2_pos)
        self.draw_O(tree3_pos)
        self.draw_O(tree4_pos)

        for i in things:
            self.board_status[i[0]][i[1]] = 1
    
    def draw_possible_moves(self):
        for i in control.possible_moves(user, brd.board):
            self.draw_dot(self.convert_map_to_logical(i))


    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(number_of_col_squares, number_of_col_squares))

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
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
    
    def draw_Pl(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_Pl_color)

    def draw_En(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_En_color)
    
    def draw_dot(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - 1, grid_position[1] - 1,
                                grid_position[0] + 1, grid_position[1] + 1, width=40,
                                outline=symbol_dot_color)
    
    def clear_cell(self, widget_id):
        self.canvas.delete(widget_id)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        #print("logical to grid pos: {}".format((size_of_board / number_of_col_squares) * logical_position + size_of_board / 18))
        return (size_of_board / number_of_col_squares) * logical_position + size_of_board / (number_of_col_squares * 2)

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        #print("grid to logical pos: {}".format(np.array(grid_position // (size_of_board / number_of_col_squares), dtype=int)))
        return np.array(grid_position // (size_of_board / number_of_col_squares), dtype=int)

    def convert_logical_to_map(self, logical_postion):
        alp = [i for i in logical_postion]
        letter = colsr.get(alp[0])
        map_position = (alp[1], letter)
        #print("logical to map pos: {}".format(map_position))
        return map_position
        
    def convert_map_to_logical(self, map_position):
        number = colsc.get(map_position[1])
        logical_position = [number, map_position[0]]
        log_pos = np.array([number, map_position[0]], dtype=int)
        #print("map to logical pos: {}".format(log_pos))
        return log_pos


    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(6):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover
    
    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        self.convert_map_to_logical(mappos)
        #brd.board = control.place(user, mappos, brd.board)

        self.show_loc(mappos)

        #print(brd.show())
        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
                else:
                    # if position on grid has an icon, return the id
                    widget_id = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
                    print(widget_id)
                    self.clear_cell(widget_id)
                    self.board_status[logical_position[0]][logical_position[1]] = 0
                    return widget_id
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns
                else:
                    # if position on grid has an icon, return the id
                    widget_id = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
                    print(widget_id)
                    self.clear_cell(widget_id)
                    self.board_status[logical_position[0]][logical_position[1]] = 0
                    return widget_id

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False
        return mappos

    def moveclick(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        mappos = self.convert_logical_to_map(logical_position)
        self.convert_map_to_logical(mappos)
        brd.board = control.place(user, mappos, brd.board)

        self.show_loc(mappos)

        print(brd.show())
        self.canvas.delete("all")
        self.play_again()
        self.draw_scenery()
        self.draw_possible_moves()
        return mappos

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
        self.board_status[logical_position[0]][logical_position[1]] = 1

        if not self.reset_board:
            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

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
        print(brd.show())
        #control.moverange(user, brd.board)

    if "place" in action:
        action = cleaninput(action, "place")
        brd.board = control.place(user, action, brd.board)
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
vis.window.after(0, get_input)
vis.mainloop()