
import tkinter as tk
from tkinter.colorchooser import askcolor
from src.controller import controller, owner
from src.context import modal_context, settings_context, color_context, unit_modal_context
from src.conversion import convert_coords
from src.grid import grid
from src.settings import symbolsize

from uibuilder.ui.components import initilise_settings

def initialise_canvas(parent, settings: settings_context):
        parent.canvas = tk.Canvas(parent.window, width=settings.var_boardsize, height=settings.var_boardsize, background=color_context().board_background)
        parent.canvas.pack(side='left',anchor='nw', fill='x')
        

def initialise_game_screen(parent, player_one, player_two, computer, settings: settings_context):
        parent.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        parent.player_one = player_one
        parent.player_two = player_two
        parent.show_stepped_on_tiles = False

        parent.game_controller = controller(player_one, player_two, computer)

        parent.statusbar = tk.Label(parent.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        parent.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        initialise_canvas(parent, settings)
        
        parent.ui = tk.Canvas(parent.window, background=color_context().ui_background)
        parent.ui.columnconfigure(0, weight=1)
        parent.ui.columnconfigure(1, weight=1)
        parent.ui.columnconfigure(2, weight=1)
        parent.ui.columnconfigure(3, weight=1)
        parent.ui.columnconfigure(4, weight=1)
        parent.ui.columnconfigure(5, weight=1)
        parent.max_ui_columns = 6
        
        parent.header_label = tk.Label(parent.ui, text="Player info", background=color_context().gray_color)

        parent.player_box = tk.Frame(parent.ui, relief=tk.RIDGE, background=color_context().black_color)

        parent.control_label = tk.Label(parent.ui, text="Controls", background=color_context().black_color)
        parent.mode_label = tk.Label(parent.ui, text="Select and move Mode", background=color_context().green_color)
        parent.action_details_label = tk.Label(parent.ui, text="Action details", background=color_context().sub_gray_color, border=3)

        parent.move_button = tk.Button(parent.ui, text="Select or move", foreground=color_context().range_move_color)
        parent.inspect_button = tk.Button(parent.ui, text="Inspect Cell", foreground=color_context().symbol_dot_color)
        parent.melee_attack_button = tk.Button(parent.ui, text="Melee Attack", foreground=color_context().red_color)
        parent.end_turn_button = tk.Button(parent.ui, text="End Turn", command=parent.end_turn)
        parent.padding_label1 = tk.Label(parent.ui, text="")
        parent.padding_label2 = tk.Label(parent.ui, text="")

        #parent.inspect_button_sub = tk.Button(parent.ui, text="Admin Inspect")
        
        parent.unit_header_label = tk.Label(parent.ui, text="Selected Unit", background=color_context().gray_color)
        parent.unit_box = tk.Frame(parent.ui, relief=tk.RIDGE)
        parent.unit_box.grid(column=0, row=20, columnspan=parent.max_ui_columns, sticky=tk.EW)

        parent.admin_header_label = tk.Label(parent.ui, text="Admin", background=color_context().gray_color)
        parent.admin_box = tk.Frame(parent.ui, relief=tk.RIDGE)
        parent.admin_box.grid(column=0, row=22, columnspan=parent.max_ui_columns, sticky=tk.EW)

        parent.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.player_box.grid(column=0, row=2, columnspan = parent.max_ui_columns)

        parent.control_label.grid(column=0, row=5,sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = parent.max_ui_columns)

        parent.move_button.grid(column=0, row=7, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.melee_attack_button.grid(column=0, row=8, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.end_turn_button.grid(column=0,sticky=tk.EW,  row=10, columnspan = parent.max_ui_columns)
        parent.inspect_button.grid(column=0, row=9, sticky=tk.EW, columnspan = parent.max_ui_columns)
 
        parent.action_details_label.grid(column=0, row=11,sticky=tk.EW, columnspan = parent.max_ui_columns, rowspan=2)

        parent.padding_label2.grid(column=0, row=13, sticky=tk.W, columnspan = 4)

        #parent.inspect_button_sub.grid(column=3, row=15, sticky=tk.W, columnspan=3)
        parent.unit_header_label.grid(column=0, row=19, sticky=tk.EW, columnspan = 6)
        parent.admin_header_label.grid(column=0, row=21, sticky=tk.EW, columnspan = 6)

        parent.move_button.bind('<Button-1>', parent.switch_mode_selectmove)
        parent.inspect_button.bind('<Button-1>', parent.switch_mode_inspect)
        parent.melee_attack_button.bind('<Button-1>', parent.switch_mode_melee_attack)
        parent.canvas.bind('<Button-1>', parent.select_move_click)

def finalise_game_screen(parent):
        parent.ui.pack(side='right',expand=True,fill='both')

def initialise_home_screen( parent, settings: settings_context, brd, gridsize):
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
                pc = owner("computer", color_context().red_color)

                parent.gridsize = settings.var_tiles
    
                gridsize.set_gridsize(parent.gridsize)
                parent.convert = convert_coords(parent.gridsize, settings.var_boardsize)
                brd.set_board(grid(parent.gridsize).setup())
                parent.initialise_game(pl1,pl2, pc, settings)
                parent.home_frame.destroy()
                
                
            
            def open_settings():
                initilise_settings(parent.window, settings, parent.initialise_home)
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

def display_gameover_screen(parent, winner: owner):
        """
        Cleans the canvas and shows the winner and score.
        """
        text = 'Winner: {}'.format(winner.name)

        parent.canvas.delete("all")
        for widget in parent.ui.winfo_children():
            widget.destroy()
        parent.ui['background'] = color_context().board_background
        parent.canvas.unbind('<Button-1>')
        parent.statusbar['text'] = ""

        parent.canvas.create_text(parent.game_settings.var_boardsize / 2, parent.game_settings.var_boardsize / 3, font="cmr 60 bold", fill=winner.color, text=text)
        score_text = 'Results \n'
        parent.canvas.create_text(parent.game_settings.var_boardsize / 2, 5 * parent.game_settings.var_boardsize / 8, font="cmr 40 bold", fill=color_context().green_color,
                                text=score_text)

        score_text = '{} Units Left: '.format(parent.game_controller.current_owner.name) + "{}".format(len(parent.game_controller.current_owner.units)) + '\n'
        score_text += '{} Units Left: '.format(parent.game_controller.other_owner.name) + "{}".format(len(parent.game_controller.other_owner.units)) + '\n'

        parent.canvas.create_text(parent.game_settings.var_boardsize / 2, 3 * parent.game_settings.var_boardsize / 4, font="cmr 30 bold", fill=color_context().green_color,
                                text=score_text)