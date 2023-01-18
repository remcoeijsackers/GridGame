
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from src.controller import controller, owner
from src.context import modal_context, settings_context, color_context, unit_modal_context
from src.conversion import convert_coords
from src.grid import grid

def initialise_home_screen( parent, settings: settings_context, brd, ui, gridsize):
            parent.home_frame = tk.Frame(parent.window, padx= 100, pady=100, relief=tk.RIDGE, width=1000, height=600)
            header_label = tk.Label(parent.home_frame, text="GridGame", font=("Courier", 44))

            entry_player_one = tk.Entry(parent.home_frame)
            entry_player_one.insert(0, 'player one')
            entry_player_one['background'] = 'orange'

            entry_player_two = tk.Entry(parent.home_frame)
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
                p = get_input()
                pl1 = owner(p[0], entry_player_one['background'])
                pl2 = owner(p[1], entry_player_two['background'])
                parent.gridsize = settings.var_tiles
    
                gridsize.set_gridsize(parent.gridsize)
                parent.convert = convert_coords(parent.gridsize, settings.var_boardsize)
                brd.set_board(grid(parent.gridsize).setup())
                parent.initialise_game(pl1,pl2, settings)
                parent.home_frame.destroy()
                
            
            def open_settings():
                ui.initilise_settings(parent.window, settings, parent.initialise_home)
                parent.home_frame.destroy()
            
            b0 = tk.Button(
                parent.home_frame,
                text='Select a Color for p1',
                command=change_color_p1, background=color_context().board_background)
            b1 = tk.Button(
                parent.home_frame,
                text='Select a Color for p2',
                command=change_color_p2, background=color_context().board_background)

            b2 = tk.Button(parent.home_frame, text="Start Game", command=start_game, background=color_context().board_background)
            settings_button = tk.Button(parent.home_frame, text="Settings",command=open_settings,background=color_context().board_background)

            header_label.grid(column=0, row=0, columnspan=3)
            entry_player_one.grid(column=0, row=1)
            entry_player_two.grid(column=0, row=2)

            b0.grid(column=1, row=1)
            b1.grid(column=1, row=2)
            settings_button.grid(column=0, row=3, columnspan=3)

            b2.grid(column=0, columnspan=3, pady=10, padx=10)
            parent.home_frame.pack()