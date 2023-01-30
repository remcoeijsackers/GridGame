
import tkinter as tk
from contexts.settingscontext import  settings_context 
from contexts import colorContext

from gamemanager.settings.settings import symbolsize

from gamemanager.players.owners import owner

def initialise_canvas(parent, settings: settings_context):
        parent.canvas = tk.Canvas(parent.window, width=settings.var_boardsize, height=settings.var_boardsize, background=colorContext.board_background)
        parent.canvas.pack(side='left',anchor='nw', fill='x')
        

def initialise_game_screen(parent, players, settings: settings_context ):
        parent.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        parent.players = players
        parent.show_stepped_on_tiles = False

        parent.statusbar = tk.Label(parent.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        parent.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        initialise_canvas(parent, settings)
        
        parent.ui = tk.Canvas(parent.window, background=colorContext.ui_background)
        parent.ui.columnconfigure(0, weight=1)
        parent.ui.columnconfigure(1, weight=1)
        parent.ui.columnconfigure(2, weight=1)
        parent.ui.columnconfigure(3, weight=1)
        parent.ui.columnconfigure(4, weight=1)
        parent.ui.columnconfigure(5, weight=1)
        parent.max_ui_columns = 6
        
        parent.header_label = tk.Label(parent.ui, text="Player info", background=colorContext.gray_color)

        parent.player_box = tk.Frame(parent.ui, relief=tk.RIDGE, background=colorContext.black_color)

        parent.control_label = tk.Label(parent.ui, text="Controls", background=colorContext.black_color)
        parent.mode_label = tk.Label(parent.ui, text="Select and move Mode", background=colorContext.green_color)
        parent.action_details_label = tk.Label(parent.ui, text="Action details", background=colorContext.sub_gray_color, border=3)

        parent.move_button = tk.Button(parent.ui, text="Select or move", foreground=colorContext.range_move_color)
        parent.inspect_button = tk.Button(parent.ui, text="Inspect Cell", foreground=colorContext.symbol_dot_color)
        parent.melee_attack_button = tk.Button(parent.ui, text="Melee Attack", foreground=colorContext.red_color)
        parent.end_turn_button = tk.Button(parent.ui, text="End Turn", command=parent.end_turn)
        parent.padding_label1 = tk.Label(parent.ui, text="")

        #parent.inspect_button_sub = tk.Button(parent.ui, text="Admin Inspect")
        
        parent.unit_header_label = tk.Label(parent.ui, text="Selected Unit", background=colorContext.gray_color)
        parent.unit_box = tk.Frame(parent.ui, relief=tk.RIDGE)
        parent.unit_box.grid(column=0, row=20, columnspan=parent.max_ui_columns, sticky=tk.EW)

        parent.admin_header_label = tk.Label(parent.ui, text="Admin", background=colorContext.gray_color)
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

        #parent.inspect_button_sub.grid(column=3, row=15, sticky=tk.W, columnspan=3)
        parent.unit_header_label.grid(column=0, row=19, sticky=tk.EW, columnspan = 6)
        parent.admin_header_label.grid(column=0, row=21, sticky=tk.EW, columnspan = 6)

        parent.move_button.bind('<Button-1>', parent.switch_mode_selectmove)
        parent.inspect_button.bind('<Button-1>', parent.switch_mode_inspect)
        parent.melee_attack_button.bind('<Button-1>', parent.switch_mode_melee_attack)
        parent.canvas.bind('<Button-1>', parent.select_move_click)

def finalise_game_screen(parent):
        parent.ui.pack(side='right',expand=True,fill='both')
        return True

def display_gameover_screen(parent, winner: owner):
        """
        Cleans the canvas and shows the winner and score.
        """
        text = 'Winner: {}'.format(winner.name)

        parent.canvas.delete("all")
        for widget in parent.ui.winfo_children():
            widget.destroy()

        parent.ui['background'] = colorContext.board_background
        parent.canvas.unbind('<Button-1>')
        parent.statusbar['text'] = ""

        parent.canvas.create_text(parent.game_settings.var_boardsize / 2, parent.game_settings.var_boardsize / 3, font="cmr 60 bold", fill=winner.color, text=text)
        score_text = 'Results \n'
        parent.canvas.create_text(parent.game_settings.var_boardsize / 2, 5 * parent.game_settings.var_boardsize / 8, font="cmr 40 bold", fill=colorContext.green_color,
                                text=score_text)

        #score_text = '{} Units Left: '.format(parent.game_controller.current_owner.name) + "{}".format(len(parent.game_controller.current_owner.units)) + '\n'
        #score_text += '{} Units Left: '.format(parent.game_controller.other_owner.name) + "{}".format(len(parent.game_controller.other_owner.units)) + '\n'

        #parent.canvas.create_text(parent.game_settings.var_boardsize / 2, 3 * parent.game_settings.var_boardsize / 4, font="cmr 30 bold", fill=colorContext.green_color,
        #                        text=score_text)