import tkinter as tk
from tkinter.colorchooser import askcolor

from contexts.settingscontext import settings_context
from contexts import colorContext
from src.conversion import convert_coords

from gamemanager.board.board import grid
from gamemanager.settings.settings import debug

from gamemanager.dm.dm import gameController
from gamemanager.players.owners import owner
from gamemanager.players.npc import npc
from uibuilder.ui.components import initilise_settings

class HomeScreen:
    def __init__(self) -> None:
        self.players = []


    def initialise_home_screen(self, parent, settings: settings_context, brd, gridsize, conversion):
            parent.home_frame = tk.Frame(parent.window, padx= 100, pady=100, relief=tk.RIDGE, width=1000, height=600)
            header_label = tk.Label(parent.home_frame, text="GridGame", font=("Courier", 44))
            def addPlayer(): 
                entry_player = tk.Entry(parent.home_frame)
                entry_player.insert(0, 'player x')
                entry_player['background'] = colorContext.red_color
                entry_player.grid(column=0)
                entry_player_control = tk.Entry(parent.home_frame)
                entry_player_control.insert(0, 'auto')
                entry_player_control.grid()

                def change_color():
                    colors = askcolor(title="Tkinter Color Chooser")
                    entry_player.configure(bg=colors[1])
                    return colors[1]

                def save_player():
                    pl = entry_player.get()
                    if entry_player_control.get() != "auto":
                        self.players.append(owner(len(self.players)+1, pl, entry_player['background']))
                    if entry_player_control.get() == "auto":
                        print("making a npc player")
                        self.players.append(npc(len(self.players)+1, pl, entry_player['background'], conversion, brd))

                butt = tk.Button(
                    parent.home_frame,
                    text='Select Color:',
                    command=change_color, 
                    background=colorContext.board_background)
                save_butt = tk.Button(
                    parent.home_frame,
                    text='Save',
                    command=save_player
                    )

                butt.grid()
                save_butt.grid()

            add_player_button = tk.Button(parent.home_frame, text="add player", command=addPlayer)

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
    
            def get_base_players():
                p1 = owner(len(self.players)+1, entry_player_one.get(), entry_player_one['background'])
                self.players.append(p1)
                p2 = owner(len(self.players)+1, entry_player_two.get(), entry_player_two['background'])
                self.players.append(p2)
            
            def start_game():

                get_base_players()
                if debug:
                    print(self.players)

                controller = gameController(self.players, parent)

                parent.gridsize = settings.var_tiles
    
                gridsize.set_gridsize(parent.gridsize)
                parent.convert = convert_coords(parent.gridsize, settings.var_boardsize)
                brd.set_board(grid(parent.gridsize).setup())
                brd.give_all_cells_coords()

                parent.initialise_game(self.players ,settings,controller)
                parent.home_frame.destroy()

                
            
            def open_settings():
                initilise_settings(parent.window, settings, parent.initialise_home)
                parent.home_frame.destroy()
            
            b0 = tk.Button(
                parent.home_frame,
                text='Select a Color for p1',
                command=change_color_p1, background=colorContext.board_background)
            b1 = tk.Button(
                parent.home_frame,
                text='Select a Color for p2',
                command=change_color_p2, background=colorContext.board_background)

            start_button = tk.Button(parent.home_frame, text="Start Game", command=start_game, background=colorContext.board_background)
            settings_button = tk.Button(parent.home_frame, text="Settings",command=open_settings,background=colorContext.board_background)

            header_label.grid(column=0, row=0, columnspan=3)
            start_button.grid(column=0, row=1, columnspan=3, pady=10, padx=10)
            settings_button.grid(column=0, row=2, columnspan=3)

            entry_player_one.grid(column=0, row=3)
            entry_player_two.grid(column=0, row=4)

            b0.grid(column=1, row=3)
            b1.grid(column=1, row=4)
            add_player_button.grid(column=5, row=3,)

            parent.home_frame.pack()