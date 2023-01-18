 def initialise_game(self, player_one, player_two, settings: settings_context):
        self.boardsize = settings.var_boardsize
        self.symbol_size = symbolsize.get_symbolsize(settings.var_boardsize)
        self.player_one = player_one
        self.player_two = player_two
        self.show_stepped_on_tiles = False

        self.game_controller = controller(player_one, player_two)

        self.statusbar = tk.Label(self.window, text="Cell info", bd=1, relief=tk.SUNKEN, anchor=tk.W)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas = tk.Canvas(self.window, width=settings.var_boardsize, height=settings.var_boardsize, background=colors.board_background)
        self.canvas.pack(side='left',anchor='nw', fill='x')
        
        self.ui = tk.Canvas(self.window, bd=1)
        self.ui.columnconfigure(0, weight=0)
        self.ui.columnconfigure(1, weight=3)
        self.max_ui_columns = 6
        
        self.header_label = tk.Label(self.ui, text="Player info", background=colors.black_color)

        self.player_box = tk.Frame(self.ui,background=colors.black_color)

        self.control_label = tk.Label(self.ui, text="Controls", background=colors.black_color)
        self.mode_label = tk.Label(self.ui, text="Select and move Mode", background=colors.green_color)
        self.action_details_label = tk.Label(self.ui, text="Action details", background=colors.gray_color)
        self.action_details_label_description = tk.Label(self.ui, text="Action details", background=colors.dark_gray_color)

        self.move_button = tk.Button(self.ui, text="Select move")
        self.inspect_button = tk.Button(self.ui, text="Inspect Cell")
        self.melee_attack_button = tk.Button(self.ui, text="Melee Attack")
        self.show_stepped_tiles_button = tk.Button(self.ui, text="show stepped tiles", command=self.show_stepped_tiles)
        self.padding_label1 = tk.Label(self.ui, text="")
        self.padding_label2 = tk.Label(self.ui, text="")

        self.end_turn_button = tk.Button(self.ui, text="End turn")
        self.inspect_button_sub = tk.Button(self.ui, text="Admin Inspect")

        self.unit_header_label = tk.Label(self.ui, text="Controlling Unit Info", background=colors.black_color)
        self.unit_box = tk.Frame(self.ui, relief=tk.RIDGE)
        self.unit_box.grid(column=0, row=20,sticky=tk.W)

        self.header_label.grid(column=0, row=0, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.player_box.grid(column=0, row=1,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.control_label.grid(column=0, row=5,sticky=tk.EW, columnspan = self.max_ui_columns)
        self.mode_label.grid(column=0, row=6,sticky=tk.EW, columnspan = self.max_ui_columns)

        self.move_button.grid(column=0, row=7, sticky=tk.W, columnspan = int(abs(self.max_ui_columns/2)))
        self.inspect_button.grid(column=0, row=10, sticky=tk.EW, columnspan = self.max_ui_columns)
        self.melee_attack_button.grid(column=int(abs(self.max_ui_columns/2)), row=7, sticky=tk.W, columnspan = int(abs(self.max_ui_columns/2)))

        #self.show_stepped_tiles_button.grid(column=0,sticky=tk.EW,  row=9, columnspan = self.max_ui_columns)
        self.action_details_label_description.grid(column=int(abs((self.max_ui_columns/2) )), row=11,sticky=tk.EW, columnspan = int(abs((self.max_ui_columns/2)+2)))
        self.action_details_label.grid(column=0, row=11,sticky=tk.EW, columnspan = int(abs((self.max_ui_columns/2)-1)))

        #self.padding_label1.grid(column=0, row=10, sticky=tk.W, columnspan = 4)
        self.padding_label2.grid(column=0, row=13, sticky=tk.W, columnspan = 4)

        
        self.end_turn_button.grid(column=0, row=15, sticky=tk.W, columnspan=3)
        self.inspect_button_sub.grid(column=3, row=15, sticky=tk.W, columnspan=3)
        self.unit_header_label.grid(column=0, row=19, sticky=tk.EW, columnspan = 6)

        self.ui.pack(side='right',anchor=tk.NW,expand=True,fill='both')
        
        self.move_button.bind('<Button-1>', self.switch_mode_selectmove)
        self.inspect_button.bind('<Button-1>', self.switch_mode_inspect)
        self.melee_attack_button.bind('<Button-1>', self.switch_mode_melee_attack)
        self.inspect_button_sub.bind('<Button-1>', self.test_modal)
        self.canvas.bind('<Button-1>', self.select_move_click)