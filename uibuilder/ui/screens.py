
import tkinter as tk
from contexts.settingscontext import  settings_context 
from contexts import colorContext

from gamemanager.settings.settings import symbolsize

from gamemanager.players.owners import owner
from uibuilder.ui.components import make_generic_event_card, make_gameevent_card

def initialise_canvas(parent, settings: settings_context):
        parent.canvas = tk.Canvas(parent.window, width=settings.var_boardsize, height=settings.var_boardsize, background=colorContext.board_background)
        parent.canvas.pack(side='left',anchor='n',fill='x')
        
def initialise_canvas_control(parent):
        btnw = 88
        btnh = 2
        # Create the containers
        parent.bottomcontrol = tk.Frame(parent.window)
        parent.leftcontrolframe =tk.Frame(parent.bottomcontrol,  background=colorContext.ui_background, highlightbackground=colorContext.black_color, highlightthickness=2)
        parent.rightcontrolframe =tk.Frame(parent.bottomcontrol,  background=colorContext.ui_background, highlightbackground=colorContext.black_color, highlightthickness=2)

        # Add the buttons and labels for the left control
        parent.control_label = tk.Label(parent.leftcontrolframe, text="Controls", background=colorContext.gray_color, width=btnw, height=btnh,highlightbackground=colorContext.black_color, highlightthickness=2)
        parent.mode_label = tk.Label(parent.leftcontrolframe, text="Select and move Mode", background=colorContext.green_color, width=btnw)
        parent.move_button = tk.Button(parent.leftcontrolframe, text="Select or move", foreground=colorContext.range_move_color, width=btnw)
        parent.inspect_button = tk.Button(parent.leftcontrolframe, text="Inspect Cell", foreground=colorContext.symbol_dot_color, width=btnw)
        parent.melee_attack_button = tk.Button(parent.leftcontrolframe, text="Melee Attack", foreground=colorContext.red_color, width=btnw)
        parent.end_turn_button = tk.Button(parent.leftcontrolframe, text="End Turn", command=parent.end_turn, width=btnw)

        # Add the components for the right control + pack them
        parent.event_label = tk.Label(parent.rightcontrolframe, text="Events", background=colorContext.gray_color, width=btnw, height=btnh)

        parent.event_label.pack(side='top',anchor='e') # pack this before the event card to make sure its on top.

        make_gameevent_card(parent, parent.rightcontrolframe)

        # pack the main container
        parent.bottomcontrol.pack(side='bottom',anchor='n',expand=True, fill='x')

        # pack the left and right containers
        parent.leftcontrolframe.pack(in_=parent.bottomcontrol, side=tk.LEFT, fill=tk.Y)
        parent.rightcontrolframe.pack(in_=parent.bottomcontrol, side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # pack the left control components
        parent.control_label.pack(side='top',anchor='w')
        parent.action_details_label = tk.Label(parent.leftcontrolframe, text="Action details", background=colorContext.ui_background,width=btnw)
        parent.action_details_label.pack(side='top',anchor='w')
        
        parent.mode_label.pack(side='top',anchor='w')
        parent.move_button.pack(side='top',anchor='w')
        parent.melee_attack_button.pack(side='top',anchor='w')
        parent.inspect_button.pack(side='top',anchor='w')
        parent.end_turn_button.pack(side='top',anchor='w')

        # bind the buttons to functions
        parent.move_button.bind('<Button-1>', parent.switch_mode_selectmove)
        parent.inspect_button.bind('<Button-1>', parent.switch_mode_inspect)
        parent.melee_attack_button.bind('<Button-1>', parent.switch_mode_melee_attack)


def initialise_game_screen(parent, players, settings: settings_context ):
        parent.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        parent.players = players
        parent.show_stepped_on_tiles = False

        parent.statusbar = tk.Label(parent.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        parent.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        initialise_canvas_control(parent)
        initialise_canvas(parent, settings)
        
        parent.ui = tk.Frame(parent.window, background=colorContext.ui_background, highlightbackground=colorContext.black_color, highlightthickness=2)
        parent.ui.columnconfigure(0, weight=1)
        parent.ui.columnconfigure(1, weight=1)
        parent.ui.columnconfigure(2, weight=1)
        parent.ui.columnconfigure(3, weight=1)
        parent.ui.columnconfigure(4, weight=1)
        parent.ui.columnconfigure(5, weight=1)
        parent.max_ui_columns = 6
        
        parent.header_label = tk.Label(parent.ui, text="Player info", background=colorContext.gray_color)

        parent.player_box = tk.Frame(parent.ui, background=colorContext.black_color)

        parent.move_button = tk.Button(parent.ui, text="Select or move", foreground=colorContext.range_move_color)
        parent.inspect_button = tk.Button(parent.ui, text="Inspect Cell", foreground=colorContext.symbol_dot_color)
        parent.melee_attack_button = tk.Button(parent.ui, text="Melee Attack", foreground=colorContext.red_color)
        parent.end_turn_button = tk.Button(parent.ui, text="End Turn", command=parent.end_turn)
        
        parent.unit_header_label = tk.Label(parent.ui, text="Selected Unit", background=colorContext.gray_color)
        parent.unit_box = tk.Frame(parent.ui)
        parent.unit_box.grid(column=0, row=20, columnspan=parent.max_ui_columns, sticky=tk.EW)

        parent.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = parent.max_ui_columns)
        parent.player_box.grid(column=0, row=2, columnspan = parent.max_ui_columns, sticky=tk.EW)

        parent.unit_header_label.grid(column=0, row=19, sticky=tk.EW, columnspan = 6)
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