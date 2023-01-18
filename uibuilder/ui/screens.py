
import tkinter as tk
from tkinter.colorchooser import askcolor
from src.controller import controller, owner
from src.context import modal_context, settings_context, color_context, unit_modal_context
from src.conversion import convert_coords
from src.grid import grid
from src.settings import symbolsize

def initialise_game_screen(parent, player_one, player_two, settings: settings_context):
        parent.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        parent.player_one = player_one
        parent.player_two = player_two
        parent.show_stepped_on_tiles = False

        parent.game_controller = controller(player_one, player_two)

        parent.statusbar = tk.Label(parent.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        parent.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        parent.canvas = tk.Canvas(parent.window, width=settings.var_boardsize, height=settings.var_boardsize, background=color_context().board_background)
        parent.canvas.pack(side='left',anchor='nw', fill='x')
        
        parent.ui = tk.Canvas(parent.window, bd=1)
        parent.ui.columnconfigure(0, weight=0)
        parent.ui.columnconfigure(1, weight=3)
        parent.max_ui_columns = 6
        
        parent.header_label = tk.Label(parent.ui, text="Player info", background=color_context().black_color)

        parent.player_box = tk.Frame(parent.ui, background=color_context().black_color)

        parent.control_label = tk.Label(parent.ui, text="Controls", background=color_context().black_color)
        parent.mode_label = tk.Label(parent.ui, text="Select and move Mode", background=color_context().green_color)
        parent.action_details_label = tk.Label(parent.ui, text="Action details", background=color_context().gray_color)
        parent.action_details_label_description = tk.Label(parent.ui, text="Action details", background=color_context().dark_gray_color)

        parent.move_button = tk.Button(parent.ui, text="Select move")
        parent.inspect_button = tk.Button(parent.ui, text="Inspect Cell")
        parent.melee_attack_button = tk.Button(parent.ui, text="Melee Attack")
        parent.show_stepped_tiles_button = tk.Button(parent.ui, text="show stepped tiles", command=parent.show_stepped_tiles)
        parent.padding_label1 = tk.Label(parent.ui, text="")
        parent.padding_label2 = tk.Label(parent.ui, text="")

        parent.end_turn_button = tk.Button(parent.ui, text="End turn")
        parent.inspect_button_sub = tk.Button(parent.ui, text="Admin Inspect")

        parent.unit_header_label = tk.Label(parent.ui, text="Controlling Unit Info", background=color_context().black_color)
        parent.unit_box = tk.Frame(parent.ui, relief=tk.RIDGE)
        parent.unit_box.grid(column=0, row=20,sticky=tk.W)

        parent.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.player_box.grid(column=0, row=1,sticky=tk.EW, columnspan = parent.max_ui_columns)

        parent.control_label.grid(column=0, row=5,sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = parent.max_ui_columns)

        parent.move_button.grid(column=0, row=7, sticky=tk.W, columnspan = int(abs(parent.max_ui_columns/2)))
        parent.inspect_button.grid(column=0, row=10, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.melee_attack_button.grid(column=int(abs(parent.max_ui_columns/2)), row=7, sticky=tk.W, columnspan = int(abs(parent.max_ui_columns/2)))

        #parent.show_stepped_tiles_button.grid(column=0,sticky=tk.EW,  row=9, columnspan = parent.max_ui_columns)
        parent.action_details_label_description.grid(column=int(abs((parent.max_ui_columns/2) )), row=11,sticky=tk.EW, columnspan = int(abs((parent.max_ui_columns/2)+2)))
        parent.action_details_label.grid(column=0, row=11,sticky=tk.EW, columnspan = int(abs((parent.max_ui_columns/2)-1)))

        #parent.padding_label1.grid(column=0, row=10, sticky=tk.W, columnspan = 4)
        parent.padding_label2.grid(column=0, row=13, sticky=tk.W, columnspan = 4)

        
        parent.end_turn_button.grid(column=0, row=15, sticky=tk.W, columnspan=3)
        parent.inspect_button_sub.grid(column=3, row=15, sticky=tk.W, columnspan=3)
        parent.unit_header_label.grid(column=0, row=19, sticky=tk.EW, columnspan = 6)

        parent.ui.pack(side='right',anchor=tk.NW,expand=True,fill='both')
        
        parent.move_button.bind('<Button-1>', parent.switch_mode_selectmove)
        parent.inspect_button.bind('<Button-1>', parent.switch_mode_inspect)
        parent.melee_attack_button.bind('<Button-1>', parent.switch_mode_melee_attack)
        parent.inspect_button_sub.bind('<Button-1>', parent.test_modal)
        parent.canvas.bind('<Button-1>', parent.select_move_click)

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