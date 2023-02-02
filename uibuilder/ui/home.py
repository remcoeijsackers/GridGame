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
import random
from objectmanager.generator import unitgenerator

class HomeScreen:
    def __init__(self) -> None:
        self.players = []

    def __addOwnerInput(self, parent, conversion, brd):
                new_player_frame = tk.Frame(parent.home_frame)

                entry_player = tk.Entry(new_player_frame)
                entry_player.insert(0, unitgenerator.get_name())
                entry_player['background'] = colorContext.red_color
                
                OPTIONS = [
                    "auto",
                    "manual",
                    ] 
                
                variable = tk.StringVar(new_player_frame)
                variable.set(OPTIONS[0])
                
                entry_player_control = tk.OptionMenu(new_player_frame, variable, *OPTIONS)
            
                def change_color():
                    colors = askcolor(title="Tkinter Color Chooser")
                    entry_player.configure(bg=colors[1])
                    return colors[1]

                def save_player():
                    pl = entry_player.get()
                    save_butt["foreground"] = colorContext.symbol_tree_color
                    save_butt["text"] = "√"
                    if variable.get() != "auto":
                        self.players.append(owner(len(self.players)+1, pl, entry_player['background']))
                    if variable.get() == "auto":
                        self.players.append(npc(len(self.players)+1, pl, entry_player['background'], conversion, brd))

                butt = tk.Button(
                    new_player_frame,
                    text='Select Color',
                    command=change_color, 
                    background=colorContext.board_background)
                save_butt = tk.Button(
                    new_player_frame,
                    text='Save',
                    command=save_player
                    )

                entry_player.grid(column=0, row=0)
                entry_player_control.grid(column=1, row=0)

                butt.grid(column=2, row=0)
                save_butt.grid(column=3,row=0)
                new_player_frame.grid(columnspan=6)

    def initialise_home_screen(self, parent, settings: settings_context, brd, gridsize, conversion):
            parent.home_frame = tk.Frame(parent.window, padx= 100, pady=100, relief=tk.RIDGE, width=1200, height=600)
            header_label = tk.Label(parent.home_frame, text="GridGame", font=("Courier", 44))
            info_label = tk.Label(parent.home_frame, text="", font=("Courier", 12))

            def addPlayer(): 
                return self.__addOwnerInput(parent, conversion, brd)

            add_player_button = tk.Button(parent.home_frame, text="add player", command=addPlayer,  width=8, height=3)

            def start_game():
                
                if len(self.players) >= 2:
                    controller = gameController(self.players, parent)
                else:
                    info_label['text'] = "Please save at least 2 players \n To start the game."
                    return

                parent.gridsize = settings.var_tiles

                gridsize.set_gridsize(parent.gridsize)
                parent.convert = convert_coords(parent.gridsize, settings.var_boardsize)
                brd.set_board(grid(parent.gridsize).setup())
                brd.give_all_cells_coords()
                parent.home_frame.destroy()
                ready = parent.initialise_game(self.players ,settings,controller)
                
                return ready

            def open_settings():
                initilise_settings(parent.window, settings, parent.initialise_home)
                parent.home_frame.destroy()
            
            start_button = tk.Button(parent.home_frame, text="Start Game", command=start_game, background=colorContext.board_background, width=20, height=5)
            settings_button = tk.Button(parent.home_frame, text="Settings",command=open_settings,background=colorContext.board_background, width=8, height=3)

            header_label.grid(column=0, row=0, columnspan=6)
            info_label.grid(column=0, row=1,columnspan=6)

            start_button.grid(column=0, row=2, columnspan=6, pady=5, padx=5)
            settings_button.grid(column=0, row=3, columnspan=6, pady=2, padx=2)

            add_player_button.grid(column=0, row=4, columnspan=6,pady=2, padx=2)

            parent.home_frame.pack()