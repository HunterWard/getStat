# gui.py
# 
# Gui Framework
# Hunter Ward
# 7/4/20

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import gui_support

count = 0

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    gui_support.set_Tk_var()
    top = MainWindow (root)
    gui_support.init(root, top)
    root.mainloop()


w = None

def create_MainWindow(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_MainWindow(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    gui_support.set_Tk_var()
    top = MainWindow (w)
    gui_support.init(w, top, *args, **kwargs)
    return (w, top)
    

def destroy_MainWindow():
    global w
    w.destroy()
    w = None

class MainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'
        _fgcolor = '#000000'  
        _compcolor = '#d9d9d9'
        _ana1color = '#d9d9d9' 
        _ana2color = '#ececec' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("120x34")
        top.minsize(120, 1)
        top.maxsize(4484, 1401)
        top.resizable(0, 0)
        top.title("FootballDB")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        # Main DB Photobox
        self.PhotoBox = tk.Canvas(top)
        self.PhotoBox.place(relx=0.646, rely=0.066, relheight=0.25
                , relwidth=0.13)
        self.PhotoBox.configure(background="#d9d9d9")
        self.PhotoBox.configure(borderwidth="2")
        self.PhotoBox.configure(highlightbackground="#d9d9d9")
        self.PhotoBox.configure(highlightcolor="black")
        self.PhotoBox.configure(insertbackground="black")
        self.PhotoBox.configure(relief="ridge")
        self.PhotoBox.configure(selectbackground="#c4c4c4")
        self.PhotoBox.configure(selectforeground="black")

        # Main DB listbox
        self.MainDBLB = ScrolledListBox(top)
        self.MainDBLB.place(relx=0.021, rely=0.067, relheight=0.425
                , relwidth=0.602)
        self.MainDBLB.configure(background="white")
        self.MainDBLB.configure(cursor="arrow")
        self.MainDBLB.configure(disabledforeground="#a3a3a3")
        self.MainDBLB.configure(font="TkFixedFont")
        self.MainDBLB.configure(foreground="black")
        self.MainDBLB.configure(highlightbackground="#d9d9d9")
        self.MainDBLB.configure(highlightcolor="#d9d9d9")
        self.MainDBLB.configure(selectbackground="#c4c4c4")
        self.MainDBLB.configure(selectforeground="black")
        self.MainDBLB.configure(selectmode='single')
        self.MainDBLB.configure(listvariable=gui_support.Empty)
        self.MainDBLB.bind('<<ListboxSelect>>',lambda e:gui_support.mainDBSelected(e, self.PlayerName, self.posVALUE, self.hwVALUE, self.bdayVALUE, self.collegeVALUE, self.teamVALUE, self.idVALUE, self.PhotoBox))

        # Player Name Label
        self.PlayerName = tk.Label(top)
        self.PlayerName.place(relx=0.781, rely=0.063, height=23, width=231)
        self.PlayerName.configure(activebackground="#f9f9f9")
        self.PlayerName.configure(activeforeground="black")
        self.PlayerName.configure(background="#d9d9d9")
        self.PlayerName.configure(disabledforeground="#a3a3a3")
        self.PlayerName.configure(foreground="#000000")
        self.PlayerName.configure(highlightbackground="#d9d9d9")
        self.PlayerName.configure(highlightcolor="black")
        self.PlayerName.configure(text='''''')

        # Menubar 
        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.sub_menu = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="File")
        self.sub_menu.add_command(
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.destroy_window(),
                font="TkMenuFont",
                foreground="#000000",
                label="Quit")
        self.sub_menu1 = tk.Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.sub_menu1,
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                foreground="#000000",
                label="Database")
        self.sub_menu1.add_command( # Clear DB
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.clearDatabase(self.MainDBLB, self.countVar),
                font="TkMenuFont",
                foreground="#000000",
                label="Clear Database")
        self.sub_menu1.add_separator(
                background="#d9d9d9")
        self.sub_menu1.add_command( # Import DB
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.importFromCSV(self.MainDBLB, self.countVar),
                font="TkMenuFont",
                foreground="#000000",
                label="Import from CSV")
        self.sub_menu1.add_command( # Export DB
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                font="TkMenuFont",
                command=lambda: gui_support.exportToCSV(),
                foreground="#000000",
                label="Export to CSV")
        self.sub_menu1.add_separator(
                background="#d9d9d9")
        self.sub_menu1.add_command( # Create new DB
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.newDB(self.MainDBLB, self.countVar),
                font="TkMenuFont",
                foreground="#000000",
                label="Create New Database")
        self.sub_menu1.add_command( # Load DB
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.loadDB(self.MainDBLB, self.countVar),
                font="TkMenuFont",
                foreground="#000000",
                label="Load Database")
        self.sub_menu1.add_command( # Refresh to regular DB View
                activebackground="#ececec",
                activeforeground="#000000",
                background="#d9d9d9",
                command=lambda: gui_support.refreshMainDB(self.MainDBLB, self.countVar),
                font="TkMenuFont",
                foreground="#000000",
                label="Refresh Database")

        # Main DB Label
        self.DBLabel = tk.Label(top)
        self.DBLabel.place(relx=0.031, rely=0.017, height=24, width=636)
        self.DBLabel.configure(activebackground="#f9f9f9")
        self.DBLabel.configure(activeforeground="black")
        self.DBLabel.configure(background="#d9d9d9")
        self.DBLabel.configure(disabledforeground="#a3a3a3")
        self.DBLabel.configure(foreground="#000000")
        self.DBLabel.configure(highlightbackground="#d9d9d9")
        self.DBLabel.configure(highlightcolor="black")
        self.DBLabel.configure(justify='left')
        self.DBLabel.configure(text='''Current Database''')

        # Notebook
        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.AddSelector = ttk.Notebook(top)
        self.AddSelector.place(relx=0.021, rely=0.834, relheight=0.151
                , relwidth=0.368)
        self.AddSelector.configure(takefocus="")
        self.AddSelector_t1_1 = tk.Frame(self.AddSelector)
        self.AddSelector.add(self.AddSelector_t1_1, padding=3)
        self.AddSelector.tab(0, text="Add Player", compound="left", underline="-1"
                ,)
        self.AddSelector_t1_1.configure(borderwidth="1")
        self.AddSelector_t1_1.configure(relief="sunken")
        self.AddSelector_t1_1.configure(background="#d9d9d9")
        self.AddSelector_t1_1.configure(highlightbackground="#d9d9d9")
        self.AddSelector_t1_1.configure(highlightcolor="black")
        self.AddSelector_t2_2 = tk.Frame(self.AddSelector)
        self.AddSelector.add(self.AddSelector_t2_2, padding=3)
        self.AddSelector.tab(1, text="Add Team", compound="left", underline="-1"
                ,)
        self.AddSelector_t2_2.configure(borderwidth="1")
        self.AddSelector_t2_2.configure(relief="sunken")
        self.AddSelector_t2_2.configure(background="#d9d9d9")
        self.AddSelector_t2_2.configure(highlightbackground="#d9d9d9")
        self.AddSelector_t2_2.configure(highlightcolor="black")

        # Player to be Added Name Label
        self.addPlayerNameLab = tk.Label(self.AddSelector_t1_1)
        self.addPlayerNameLab.place(relx=0.018, rely=0.167, height=25, width=96)
        self.addPlayerNameLab.configure(activebackground="#f9f9f9")
        self.addPlayerNameLab.configure(activeforeground="black")
        self.addPlayerNameLab.configure(background="#d9d9d9")
        self.addPlayerNameLab.configure(disabledforeground="#a3a3a3")
        self.addPlayerNameLab.configure(foreground="#000000")
        self.addPlayerNameLab.configure(highlightbackground="#d9d9d9")
        self.addPlayerNameLab.configure(highlightcolor="black")
        self.addPlayerNameLab.configure(text='''Player Name:''')

        # Player to be added Entry Box
        self.playerNameEntry = tk.Entry(self.AddSelector_t1_1)
        self.playerNameEntry.place(relx=0.265, rely=0.179, height=20
                , relwidth=0.316)
        self.playerNameEntry.configure(background="white")
        self.playerNameEntry.configure(disabledforeground="#a3a3a3")
        self.playerNameEntry.configure(font="TkFixedFont")
        self.playerNameEntry.configure(foreground="#000000")
        self.playerNameEntry.configure(highlightbackground="#d9d9d9")
        self.playerNameEntry.configure(highlightcolor="black")
        self.playerNameEntry.configure(insertbackground="black")
        self.playerNameEntry.configure(selectbackground="#c4c4c4")
        self.playerNameEntry.configure(selectforeground="black")
        self.playerNameEntry.bind('<FocusOut>',lambda e:gui_support.playerSearchNameFocusOUT(e))

        # Position of player to be added
        self.addPlayerPosLab = tk.Label(self.AddSelector_t1_1)
        self.addPlayerPosLab.place(relx=0.028, rely=0.607, height=26, width=88)
        self.addPlayerPosLab.configure(activebackground="#f9f9f9")
        self.addPlayerPosLab.configure(activeforeground="black")
        self.addPlayerPosLab.configure(background="#d9d9d9")
        self.addPlayerPosLab.configure(disabledforeground="#a3a3a3")
        self.addPlayerPosLab.configure(foreground="#000000")
        self.addPlayerPosLab.configure(highlightbackground="#d9d9d9")
        self.addPlayerPosLab.configure(highlightcolor="black")
        self.addPlayerPosLab.configure(text='''Position (Op):''')

        # Player position combobox
        self.playerPositionCB = ttk.Combobox(self.AddSelector_t1_1)
        self.playerPositionCB.place(relx=0.265, rely=0.524, relheight=0.464
                , relwidth=0.186)
        self.value_list = ['Any','QB','RB','FB','WR','TE','T','G','C','DE','DT','ROLB','LOLB','OLB','ILB','CB','SS','FS','S','P','K','LS',]
        self.playerPositionCB.configure(values=self.value_list)
        self.playerPositionCB.current(newindex=0)
        self.playerPositionCB.bind('<FocusOut>',lambda e:gui_support.playerSearchPosFocusOUT(e))

        # Player add search button
        self.playerSearchBTN = tk.Button(self.AddSelector_t1_1)
        self.playerSearchBTN.place(relx=0.796, rely=0.333, height=24, width=46)
        self.playerSearchBTN.configure(activebackground="#ececec")
        self.playerSearchBTN.configure(activeforeground="#000000")
        self.playerSearchBTN.configure(background="#d9d9d9")
        self.playerSearchBTN.configure(disabledforeground="#a3a3a3")
        self.playerSearchBTN.configure(foreground="#000000")
        self.playerSearchBTN.configure(highlightbackground="#d9d9d9")
        self.playerSearchBTN.configure(highlightcolor="black")
        self.playerSearchBTN.configure(pady="0")
        self.playerSearchBTN.configure(text='''Search''')
        self.playerSearchBTN.bind('<Button-1>',lambda e:gui_support.playerSearchBTNPress(e, self.searchLB, self.countVar))

        # Add Team label
        self.addTeamTeamLab = tk.Label(self.AddSelector_t2_2)
        self.addTeamTeamLab.place(relx=0.061, rely=0.19, height=25, width=44)
        self.addTeamTeamLab.configure(activebackground="#f9f9f9")
        self.addTeamTeamLab.configure(activeforeground="black")
        self.addTeamTeamLab.configure(background="#d9d9d9")
        self.addTeamTeamLab.configure(disabledforeground="#a3a3a3")
        self.addTeamTeamLab.configure(foreground="#000000")
        self.addTeamTeamLab.configure(highlightbackground="#d9d9d9")
        self.addTeamTeamLab.configure(highlightcolor="black")
        self.addTeamTeamLab.configure(text='''Team:''')

        # Add team year label
        self.addTeamYearLab = tk.Label(self.AddSelector_t2_2)
        self.addTeamYearLab.place(relx=0.074, rely=0.631, height=26, width=37)
        self.addTeamYearLab.configure(activebackground="#f9f9f9")
        self.addTeamYearLab.configure(activeforeground="black")
        self.addTeamYearLab.configure(background="#d9d9d9")
        self.addTeamYearLab.configure(disabledforeground="#a3a3a3")
        self.addTeamYearLab.configure(foreground="#000000")
        self.addTeamYearLab.configure(highlightbackground="#d9d9d9")
        self.addTeamYearLab.configure(highlightcolor="black")
        self.addTeamYearLab.configure(text='''Year:''')

        # Select Team Combobox
        self.teamSelectCB = ttk.Combobox(self.AddSelector_t2_2)
        self.teamSelectCB.place(relx=0.178, rely=0.143, relheight=0.464
                , relwidth=0.42)
        self.value_list = ['49ers','Bears','Bengals','Bills','Broncos','Browns','Buccaneers','Cardinals','Chargers','Chiefs','Colts','Cowboys','Dolphins','Eagles','Falcons','Giants','Jaguars','Jets','Lions','Packers','Panthers','Patriots','Raiders','Rams','Ravens','Saints','Seahawks','Steelers','Texans','Titans','Washington','Vikings',]
        self.teamSelectCB.configure(values=self.value_list)
        self.teamSelectCB.current(newindex=0)
        self.teamSelectCB.bind('<FocusOut>',lambda e:gui_support.teamSearchTeamFocusOUT(e))

        # Team year entrybox
        self.teamYearEntry = tk.Entry(self.AddSelector_t2_2)
        self.teamYearEntry.place(relx=0.176, rely=0.631, height=20
                , relwidth=0.214)
        self.teamYearEntry.configure(background="white")
        self.teamYearEntry.configure(disabledforeground="#a3a3a3")
        self.teamYearEntry.configure(font="TkFixedFont")
        self.teamYearEntry.configure(foreground="#000000")
        self.teamYearEntry.configure(highlightbackground="#d9d9d9")
        self.teamYearEntry.configure(highlightcolor="black")
        self.teamYearEntry.configure(insertbackground="black")
        self.teamYearEntry.configure(selectbackground="#c4c4c4")
        self.teamYearEntry.configure(selectforeground="black")
        self.teamYearEntry.bind('<Enter>',lambda e:gui_support.teamSearchYearFocusOUT(e))

        # Add teeam search button
        self.teamSearchBTN = tk.Button(self.AddSelector_t2_2)
        self.teamSearchBTN.place(relx=0.796, rely=0.333, height=24, width=46)
        self.teamSearchBTN.configure(activebackground="#ececec")
        self.teamSearchBTN.configure(activeforeground="#000000")
        self.teamSearchBTN.configure(background="#d9d9d9")
        self.teamSearchBTN.configure(disabledforeground="#a3a3a3")
        self.teamSearchBTN.configure(foreground="#000000")
        self.teamSearchBTN.configure(highlightbackground="#d9d9d9")
        self.teamSearchBTN.configure(highlightcolor="black")
        self.teamSearchBTN.configure(pady="0")
        self.teamSearchBTN.configure(text='''Search''')
        self.teamSearchBTN.bind('<Button-1>',lambda e:gui_support.teamSearchBTNPress(e, self.searchLB))

        # Position label
        self.PosLab = tk.Label(top)
        self.PosLab.place(relx=0.781, rely=0.19, height=24, width=56)
        self.PosLab.configure(activebackground="#f9f9f9")
        self.PosLab.configure(activeforeground="black")
        self.PosLab.configure(background="#d9d9d9")
        self.PosLab.configure(disabledforeground="#a3a3a3")
        self.PosLab.configure(foreground="#000000")
        self.PosLab.configure(highlightbackground="#d9d9d9")
        self.PosLab.configure(highlightcolor="black")
        self.PosLab.configure(text='''Position:''')

        # Team label
        self.teamLab = tk.Label(top)
        self.teamLab.place(relx=0.792, rely=0.22, height=24, width=50)
        self.teamLab.configure(activebackground="#f9f9f9")
        self.teamLab.configure(activeforeground="black")
        self.teamLab.configure(background="#d9d9d9")
        self.teamLab.configure(disabledforeground="#a3a3a3")
        self.teamLab.configure(foreground="#000000")
        self.teamLab.configure(highlightbackground="#d9d9d9")
        self.teamLab.configure(highlightcolor="black")
        self.teamLab.configure(text='''Team:''')

        # Birthday label
        self.bdayLab = tk.Label(top)
        self.bdayLab.place(relx=0.796, rely=0.095, height=24, width=37)
        self.bdayLab.configure(activebackground="#f9f9f9")
        self.bdayLab.configure(activeforeground="black")
        self.bdayLab.configure(background="#d9d9d9")
        self.bdayLab.configure(disabledforeground="#a3a3a3")
        self.bdayLab.configure(foreground="#000000")
        self.bdayLab.configure(highlightbackground="#d9d9d9")
        self.bdayLab.configure(highlightcolor="black")
        self.bdayLab.configure(text='''Born:''')

        # Height/Weight label
        self.hwLab = tk.Label(top)
        self.hwLab.place(relx=0.799, rely=0.127, height=24, width=31)
        self.hwLab.configure(activebackground="#f9f9f9")
        self.hwLab.configure(activeforeground="black")
        self.hwLab.configure(background="#d9d9d9")
        self.hwLab.configure(disabledforeground="#a3a3a3")
        self.hwLab.configure(foreground="#000000")
        self.hwLab.configure(highlightbackground="#d9d9d9")
        self.hwLab.configure(highlightcolor="black")
        self.hwLab.configure(text='''H/W:''')

        # College Label
        self.collegeLab = tk.Label(top)
        self.collegeLab.place(relx=0.781, rely=0.16, height=23, width=54)
        self.collegeLab.configure(activebackground="#f9f9f9")
        self.collegeLab.configure(activeforeground="black")
        self.collegeLab.configure(background="#d9d9d9")
        self.collegeLab.configure(disabledforeground="#a3a3a3")
        self.collegeLab.configure(foreground="#000000")
        self.collegeLab.configure(highlightbackground="#d9d9d9")
        self.collegeLab.configure(highlightcolor="black")
        self.collegeLab.configure(text='''College:''')

        # playerID label
        self.pIdLab = tk.Label(top)
        self.pIdLab.place(relx=0.779, rely=0.249, height=24, width=61)
        self.pIdLab.configure(activebackground="#f9f9f9")
        self.pIdLab.configure(activeforeground="black")
        self.pIdLab.configure(background="#d9d9d9")
        self.pIdLab.configure(disabledforeground="#a3a3a3")
        self.pIdLab.configure(foreground="#000000")
        self.pIdLab.configure(highlightbackground="#d9d9d9")
        self.pIdLab.configure(highlightcolor="black")
        self.pIdLab.configure(text='''PlayerID:''')

        # Add player picture canvas
        self.AddCanvas = tk.Canvas(top)
        self.AddCanvas.place(relx=0.458, rely=0.571, relheight=0.175
                , relwidth=0.094)
        self.AddCanvas.configure(background="#d9d9d9")
        self.AddCanvas.configure(borderwidth="2")
        self.AddCanvas.configure(highlightbackground="#d9d9d9")
        self.AddCanvas.configure(highlightcolor="black")
        self.AddCanvas.configure(insertbackground="black")
        self.AddCanvas.configure(relief="ridge")
        self.AddCanvas.configure(selectbackground="#c4c4c4")
        self.AddCanvas.configure(selectforeground="black")

        # Search Listbox
        self.searchLB = ScrolledListBox(top)
        self.searchLB.place(relx=0.021, rely=0.574, relheight=0.246
                , relwidth=0.367)
        self.searchLB.configure(background="white")
        self.searchLB.configure(cursor="arrow")
        self.searchLB.configure(disabledforeground="#a3a3a3")
        self.searchLB.configure(font="TkFixedFont")
        self.searchLB.configure(foreground="black")
        self.searchLB.configure(highlightbackground="#d9d9d9")
        self.searchLB.configure(highlightcolor="#d9d9d9")
        self.searchLB.configure(selectbackground="#c4c4c4")
        self.searchLB.configure(selectforeground="black")
        self.searchLB.configure(selectmode='single')
        self.searchLB.configure(setgrid="1")
        self.searchLB.bind('<<ListboxSelect>>',lambda e:gui_support.searchLBSelected(e, self.searchNameVALUE, self.searchPosVALUE, self.Label1, self.bdaySearchVALUE, self.collegeSearchVALUE, self.teamsearchVALUE, self.pidsearchVALUE, self.AddCanvas))

        # Add to database label
        self.addToDBLAB = tk.Label(top)
        self.addToDBLAB.place(relx=0.021, rely=0.524, height=24, width=646)
        self.addToDBLAB.configure(activebackground="#f9f9f9")
        self.addToDBLAB.configure(activeforeground="black")
        self.addToDBLAB.configure(background="#d9d9d9")
        self.addToDBLAB.configure(disabledforeground="#a3a3a3")
        self.addToDBLAB.configure(foreground="#000000")
        self.addToDBLAB.configure(highlightbackground="#d9d9d9")
        self.addToDBLAB.configure(highlightcolor="black")
        self.addToDBLAB.configure(text='''Add to Database''')

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.021, rely=0.508, relwidth=0.604)

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.625, rely=0.508, relheight=0.477)
        self.TSeparator2.configure(orient="vertical")

        self.TSeparator3 = ttk.Separator(top)
        self.TSeparator3.place(relx=0.646, rely=0.38, relwidth=0.331)

        # Birthday value label
        self.bdayVALUE = tk.Label(top)
        self.bdayVALUE.place(relx=0.833, rely=0.095, height=24, width=166)
        self.bdayVALUE.configure(activebackground="#f9f9f9")
        self.bdayVALUE.configure(activeforeground="black")
        self.bdayVALUE.configure(background="#d9d9d9")
        self.bdayVALUE.configure(disabledforeground="#a3a3a3")
        self.bdayVALUE.configure(foreground="#000000")
        self.bdayVALUE.configure(highlightbackground="#d9d9d9")
        self.bdayVALUE.configure(highlightcolor="black")
        self.bdayVALUE.configure(text='''''')

        # Height/weight value label
        self.hwVALUE = tk.Label(top)
        self.hwVALUE.place(relx=0.831, rely=0.128, height=25, width=167)
        self.hwVALUE.configure(activebackground="#f9f9f9")
        self.hwVALUE.configure(activeforeground="black")
        self.hwVALUE.configure(background="#d9d9d9")
        self.hwVALUE.configure(disabledforeground="#a3a3a3")
        self.hwVALUE.configure(foreground="#000000")
        self.hwVALUE.configure(highlightbackground="#d9d9d9")
        self.hwVALUE.configure(highlightcolor="black")
        self.hwVALUE.configure(text='''''')

        # College value label
        self.collegeVALUE = tk.Label(top)
        self.collegeVALUE.place(relx=0.833, rely=0.16, height=24, width=166)
        self.collegeVALUE.configure(activebackground="#f9f9f9")
        self.collegeVALUE.configure(activeforeground="black")
        self.collegeVALUE.configure(background="#d9d9d9")
        self.collegeVALUE.configure(disabledforeground="#a3a3a3")
        self.collegeVALUE.configure(foreground="#000000")
        self.collegeVALUE.configure(highlightbackground="#d9d9d9")
        self.collegeVALUE.configure(highlightcolor="black")
        self.collegeVALUE.configure(text='''''')

        # Position value label
        self.posVALUE = tk.Label(top)
        self.posVALUE.place(relx=0.833, rely=0.19, height=24, width=166)
        self.posVALUE.configure(activebackground="#f9f9f9")
        self.posVALUE.configure(activeforeground="black")
        self.posVALUE.configure(background="#d9d9d9")
        self.posVALUE.configure(disabledforeground="#a3a3a3")
        self.posVALUE.configure(foreground="#000000")
        self.posVALUE.configure(highlightbackground="#d9d9d9")
        self.posVALUE.configure(highlightcolor="black")
        self.posVALUE.configure(text='''''')

        # Team value label
        self.teamVALUE = tk.Label(top)
        self.teamVALUE.place(relx=0.833, rely=0.22, height=25, width=166)
        self.teamVALUE.configure(activebackground="#f9f9f9")
        self.teamVALUE.configure(activeforeground="black")
        self.teamVALUE.configure(background="#d9d9d9")
        self.teamVALUE.configure(disabledforeground="#a3a3a3")
        self.teamVALUE.configure(foreground="#000000")
        self.teamVALUE.configure(highlightbackground="#d9d9d9")
        self.teamVALUE.configure(highlightcolor="black")
        self.teamVALUE.configure(text='''''')

        # playerID value label
        self.idVALUE = tk.Label(top)
        self.idVALUE.place(relx=0.833, rely=0.248, height=25, width=169)
        self.idVALUE.configure(activebackground="#f9f9f9")
        self.idVALUE.configure(activeforeground="black")
        self.idVALUE.configure(background="#d9d9d9")
        self.idVALUE.configure(disabledforeground="#a3a3a3")
        self.idVALUE.configure(foreground="#000000")
        self.idVALUE.configure(highlightbackground="#d9d9d9")
        self.idVALUE.configure(highlightcolor="black")
        self.idVALUE.configure(text='''''')

        # Searched name value
        self.searchNameVALUE = tk.Label(top)
        self.searchNameVALUE.place(relx=0.395, rely=0.739, height=24, width=242)
        self.searchNameVALUE.configure(activebackground="#f9f9f9")
        self.searchNameVALUE.configure(activeforeground="black")
        self.searchNameVALUE.configure(background="#d9d9d9")
        self.searchNameVALUE.configure(disabledforeground="#a3a3a3")
        self.searchNameVALUE.configure(foreground="#000000")
        self.searchNameVALUE.configure(highlightbackground="#d9d9d9")
        self.searchNameVALUE.configure(highlightcolor="black")
        self.searchNameVALUE.configure(text='''''')

        # Search info box
        self.searchInfoBOX = tk.LabelFrame(top)
        self.searchInfoBOX.place(relx=0.406, rely=0.77, relheight=0.154
                , relwidth=0.206)
        self.searchInfoBOX.configure(relief='sunken')
        self.searchInfoBOX.configure(foreground="black")
        self.searchInfoBOX.configure(relief="sunken")
        self.searchInfoBOX.configure(text='''Info''')
        self.searchInfoBOX.configure(background="#d9d9d9")
        self.searchInfoBOX.configure(cursor="fleur")
        self.searchInfoBOX.configure(highlightbackground="#d9d9d9")
        self.searchInfoBOX.configure(highlightcolor="black")

        # Birthday search value label
        self.bdaySearchVALUE = tk.Label(self.searchInfoBOX)
        self.bdaySearchVALUE.place(relx=0.202, rely=0.107, height=25, width=128
                , bordermode='ignore')
        self.bdaySearchVALUE.configure(activebackground="#f9f9f9")
        self.bdaySearchVALUE.configure(activeforeground="black")
        self.bdaySearchVALUE.configure(background="#d9d9d9")
        self.bdaySearchVALUE.configure(disabledforeground="#a3a3a3")
        self.bdaySearchVALUE.configure(foreground="#000000")
        self.bdaySearchVALUE.configure(highlightbackground="#d9d9d9")
        self.bdaySearchVALUE.configure(highlightcolor="black")
        self.bdaySearchVALUE.configure(text='''''')

        # College search value label
        self.collegeSearchVALUE = tk.Label(self.searchInfoBOX)
        self.collegeSearchVALUE.place(relx=0.031, rely=0.321, height=25
                , width=207, bordermode='ignore')
        self.collegeSearchVALUE.configure(activebackground="#f9f9f9")
        self.collegeSearchVALUE.configure(activeforeground="black")
        self.collegeSearchVALUE.configure(background="#d9d9d9")
        self.collegeSearchVALUE.configure(disabledforeground="#a3a3a3")
        self.collegeSearchVALUE.configure(foreground="#000000")
        self.collegeSearchVALUE.configure(highlightbackground="#d9d9d9")
        self.collegeSearchVALUE.configure(highlightcolor="black")
        self.collegeSearchVALUE.configure(text='''''')

        # Team search value label 
        self.teamsearchVALUE = tk.Label(self.searchInfoBOX)
        self.teamsearchVALUE.place(relx=0.049, rely=0.536, height=25, width=196
                , bordermode='ignore')
        self.teamsearchVALUE.configure(activebackground="#f9f9f9")
        self.teamsearchVALUE.configure(activeforeground="black")
        self.teamsearchVALUE.configure(background="#d9d9d9")
        self.teamsearchVALUE.configure(disabledforeground="#a3a3a3")
        self.teamsearchVALUE.configure(foreground="#000000")
        self.teamsearchVALUE.configure(highlightbackground="#d9d9d9")
        self.teamsearchVALUE.configure(highlightcolor="black")
        self.teamsearchVALUE.configure(text='''''')

        # playerID Search value label
        self.pidsearchVALUE = tk.Label(self.searchInfoBOX)
        self.pidsearchVALUE.place(relx=0.054, rely=0.741, height=25, width=197
                , bordermode='ignore')
        self.pidsearchVALUE.configure(activebackground="#f9f9f9")
        self.pidsearchVALUE.configure(activeforeground="black")
        self.pidsearchVALUE.configure(background="#d9d9d9")
        self.pidsearchVALUE.configure(disabledforeground="#a3a3a3")
        self.pidsearchVALUE.configure(foreground="#000000")
        self.pidsearchVALUE.configure(highlightbackground="#d9d9d9")
        self.pidsearchVALUE.configure(highlightcolor="black")
        self.pidsearchVALUE.configure(text='''''')

        # Delete from main DB Button
        self.deleteBTN = tk.Button(top)
        self.deleteBTN.place(relx=0.802, rely=0.308, height=24, width=157)
        self.deleteBTN.configure(activebackground="#ececec")
        self.deleteBTN.configure(activeforeground="#000000")
        self.deleteBTN.configure(background="#d9d9d9")
        self.deleteBTN.configure(disabledforeground="#a3a3a3")
        self.deleteBTN.configure(foreground="#000000")
        self.deleteBTN.configure(highlightbackground="#d9d9d9")
        self.deleteBTN.configure(highlightcolor="black")
        self.deleteBTN.configure(pady="0")
        self.deleteBTN.configure(text='''Delete Entry''')
        self.deleteBTN.bind('<Button-1>',lambda e:gui_support.deleteEntryPress(e, self.MainDBLB, self.countVar))

        # Search position value label value
        self.searchPosVALUE = tk.Label(top)
        self.searchPosVALUE.place(relx=0.552, rely=0.574, height=25, width=73)
        self.searchPosVALUE.configure(activebackground="#f9f9f9")
        self.searchPosVALUE.configure(activeforeground="black")
        self.searchPosVALUE.configure(background="#d9d9d9")
        self.searchPosVALUE.configure(disabledforeground="#a3a3a3")
        self.searchPosVALUE.configure(foreground="#000000")
        self.searchPosVALUE.configure(highlightbackground="#d9d9d9")
        self.searchPosVALUE.configure(highlightcolor="black")
        self.searchPosVALUE.configure(text='''''')


        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.552, rely=0.607, height=25, width=73)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''''')

        # Filter label
        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.627, rely=0.393, height=24, width=400)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Filter''')

        # Filter player name
        self.pnameFILTER = tk.Entry(top)
        self.pnameFILTER.place(relx=0.688, rely=0.475, height=20, relwidth=0.217)

        self.pnameFILTER.configure(background="white")
        self.pnameFILTER.configure(disabledforeground="#a3a3a3")
        self.pnameFILTER.configure(font="TkFixedFont")
        self.pnameFILTER.configure(foreground="#000000")
        self.pnameFILTER.configure(highlightbackground="#d9d9d9")
        self.pnameFILTER.configure(highlightcolor="black")
        self.pnameFILTER.configure(insertbackground="black")
        self.pnameFILTER.configure(selectbackground="#c4c4c4")
        self.pnameFILTER.configure(selectforeground="black")
        self.pnameFILTER.bind('<FocusOut>',lambda e:gui_support.filterNameFocusOUT(e))

        # Filter playername label
        self.filterpname = tk.Label(top)
        self.filterpname.place(relx=0.688, rely=0.443, height=25, width=265)
        self.filterpname.configure(activebackground="#f9f9f9")
        self.filterpname.configure(activeforeground="black")
        self.filterpname.configure(background="#d9d9d9")
        self.filterpname.configure(disabledforeground="#a3a3a3")
        self.filterpname.configure(foreground="#000000")
        self.filterpname.configure(highlightbackground="#d9d9d9")
        self.filterpname.configure(highlightcolor="black")
        self.filterpname.configure(text='''Player Name''')

        # Position filter value
        self.posFilterCB = ttk.Combobox(top)
        self.posFilterCB.place(relx=0.688, rely=0.558, relheight=0.051
                , relwidth=0.069)
        self.value_list = ['Any', 'QB','RB','FB','WR','TE','T','G','C','DE','DT','ROLB','LOLB','OLB','ILB','CB','SS','FS','S','P','K','LS',]
        self.posFilterCB.configure(values=self.value_list)
        self.posFilterCB.current(newindex=0)
        self.posFilterCB.bind('<FocusOut>',lambda e:gui_support.filterPosFocusOUT(e))

        # Team filter combobox
        self.teamCBFilter = ttk.Combobox(top)
        self.teamCBFilter.place(relx=0.781, rely=0.558, relheight=0.051
                , relwidth=0.149)
        self.value_list = ['Any', '49ers','Bears','Bengals','Bills','Broncos','Browns','Buccaneers','Cardinals','Chargers','Chiefs','Colts','Cowboys','Dolphins','Eagles','Falcons','Giants','Jaguars','Jets','Lions','Packers','Panthers','Patriots','Raiders','Rams','Ravens','Saints','Seahawks','Steelers','Texans','Titans','Washington','Vikings', 'FA/R']
        self.teamCBFilter.configure(values=self.value_list)
        self.teamCBFilter.current(newindex=0)
        self.teamCBFilter.bind('<FocusOut>',lambda e:gui_support.filterTeamFocusOUT(e))

        # Position filter label
        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.685, rely=0.536, height=13, width=81)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''Position''')

        # Team filter label
        self.Label4 = tk.Label(top)
        self.Label4.place(relx=0.78, rely=0.538, height=13, width=162)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(text='''Team''')

        # Filter button
        self.filterBTN = tk.Button(top)
        self.filterBTN.place(relx=0.828, rely=0.713, height=24, width=97)
        self.filterBTN.configure(activebackground="#ececec")
        self.filterBTN.configure(activeforeground="#000000")
        self.filterBTN.configure(background="#d9d9d9")
        self.filterBTN.configure(disabledforeground="#a3a3a3")
        self.filterBTN.configure(foreground="#000000")
        self.filterBTN.configure(highlightbackground="#d9d9d9")
        self.filterBTN.configure(highlightcolor="black")
        self.filterBTN.configure(pady="0")
        self.filterBTN.configure(text='''Filter''')
        self.filterBTN.bind('<Button-1>',lambda e:gui_support.filterBTNPress(e, self.MainDBLB, self.countVar))

        # Filter to CSV
        self.filtertoCSVBTN = tk.Button(top)
        self.filtertoCSVBTN.place(relx=0.688, rely=0.711, height=24, width=117)
        self.filtertoCSVBTN.configure(activebackground="#ececec")
        self.filtertoCSVBTN.configure(activeforeground="#000000")
        self.filtertoCSVBTN.configure(background="#d9d9d9")
        self.filtertoCSVBTN.configure(disabledforeground="#a3a3a3")
        self.filtertoCSVBTN.configure(foreground="#000000")
        self.filtertoCSVBTN.configure(highlightbackground="#d9d9d9")
        self.filtertoCSVBTN.configure(highlightcolor="black")
        self.filtertoCSVBTN.configure(pady="0")
        self.filtertoCSVBTN.configure(text='''Filter to CSV''')
        self.filtertoCSVBTN.bind('<Button-1>',lambda e:gui_support.filterToCsvBTNPress(e))

        # Add to DB Button
        self.addBTN = tk.Button(top)
        self.addBTN.place(relx=0.426, rely=0.949, height=24, width=33)
        self.addBTN.configure(activebackground="#ececec")
        self.addBTN.configure(activeforeground="#000000")
        self.addBTN.configure(background="#d9d9d9")
        self.addBTN.configure(disabledforeground="#a3a3a3")
        self.addBTN.configure(foreground="#000000")
        self.addBTN.configure(highlightbackground="#d9d9d9")
        self.addBTN.configure(highlightcolor="black")
        self.addBTN.configure(pady="0")
        self.addBTN.configure(text='''Add''')
        self.addBTN.bind('<Button-1>',lambda e:gui_support.addPlayerToDB(e, self.MainDBLB, self.countVar))

        # Add all to DB button
        self.addAllBTN = tk.Button(top)
        self.addAllBTN.place(relx=0.528, rely=0.949, height=24, width=50)
        self.addAllBTN.configure(activebackground="#ececec")
        self.addAllBTN.configure(activeforeground="#000000")
        self.addAllBTN.configure(background="#d9d9d9")
        self.addAllBTN.configure(disabledforeground="#a3a3a3")
        self.addAllBTN.configure(foreground="#000000")
        self.addAllBTN.configure(highlightbackground="#d9d9d9")
        self.addAllBTN.configure(highlightcolor="black")
        self.addAllBTN.configure(pady="0")
        self.addAllBTN.configure(text='''Add All''')
        self.addAllBTN.bind('<Button-1>',lambda e:gui_support.addAllToDB(e, self.MainDBLB,self.countVar))

        # DB Count variable label
        self.countVar = tk.Label(top)
        self.countVar.place(relx=0.454, rely=0.015, height=31, width=163)
        self.countVar.configure(background="#d9d9d9")
        self.countVar.configure(disabledforeground="#a3a3a3")
        self.countVar.configure(foreground="#000000")
        self.countVar.configure(text='''count''')

        try:
            gui_support.refreshMainDB(self.MainDBLB, self.countVar)
        except:
            print('No tables')

    @staticmethod
    def popup1(event, *args, **kwargs):
        Popupmenu1 = tk.Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#f9f9f9")
        Popupmenu1.configure(activeborderwidth="1")
        Popupmenu1.configure(activeforeground="black")
        Popupmenu1.configure(background="#d9d9d9")
        Popupmenu1.configure(borderwidth="1")
        Popupmenu1.configure(disabledforeground="#a3a3a3")
        Popupmenu1.configure(font="{Segoe UI} 9")
        Popupmenu1.configure(foreground="black")
        Popupmenu1.post(event.x_root, event.y_root)

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

if __name__ == '__main__':
    vp_start_gui()





