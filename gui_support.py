# gui_support.py
#
# Contains backend for GUI
# Hunter Ward
# 7/10/20

import sys
from getStat import getStats
from variables import guiVars
import sqlite3
from PIL import Image, ImageTk
import urllib
import io
import csv
import PIL
from tkinter import filedialog

stats = getStats()
guiV = guiVars()
# create default database
dbname = 'DBFiles/default.db'
conn = sqlite3.connect(dbname, isolation_level=None)
conn.execute('PRAGMA foreign_keys = ON')
images = []
count = None
query = None

teamABV = {'Cardinals': 'crd', 'Falcons': 'atl',
                'Ravens': 'rav', 'Bills': 'buf',
                'Panthers': 'car', 'Bears': 'chi',
                'Bengals': 'cin', 'Browns': 'cle',
                'Cowboys': 'dal', 'Broncos': 'den',
                'Lions': 'det', 'Packers': 'gnb',
                'Texans': 'htx', 'Colts': 'clt',
                'Jaguars': 'jax', 'Chiefs': 'kan',
                'Chargers': 'sdg', 'Rams': 'ram',
                'Dolphins': 'mia', 'Vikings': 'min',
                'Patriots': 'nwe', 'Saints': 'nor',
                'Giants': 'nyg', 'Jets': 'nyj',
                'Raiders': 'rai', 'Eagles': 'phi',
                'Steelers': 'pit', '49ers': 'sfo',
                'Seahawks': 'sea', 'Buccaneers': 'tam',
                'Titans': 'oti', 'Washington': 'was', 'FA/R': 'FA/R'}

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

def set_Tk_var():
    global Empty
    Empty = tk.StringVar()
    global addPPosSearchCB
    addPPosSearchCB = tk.StringVar()
    global combobox
    combobox = tk.StringVar()
    global posFilterCB
    posFilterCB = tk.StringVar()
    global teamFilterCB
    teamFilterCB = tk.StringVar()
    global divFilterCB
    divFilterCB = tk.StringVar()

def init(top, gui, *args, **kwargs):
    
    global w, top_level, root
    w = gui
    top_level = top
    root = top


# Deletes entry from main DB
# Cascade deletion takes care of all relations
def deleteEntryPress(p1, mdblb, count):
    print('gui_support.deleteEntryPress')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM player WHERE player.playerID = (?)', (guiV.mainDBSelectPiD, ))
    cursor.close()
    

    refreshMainDB(mdblb, count)
    sys.stdout.flush()

# Filters main DB listbox to only show filtered data
def filterBTNPress(p1, mdblb, count):
    print('gui_support.filterBTNPress')

    cursor = conn.cursor()
    queryName = None
    queryPos = None
    queryTeam = None
    global query
    query = 'SELECT DISTINCT player.playerID, player.name FROM player INNER JOIN playsfor ON playsfor.playerID = player.playerID INNER JOIN isa ON isa.playerID = player.playerID WHERE '
    endQ = 'ORDER BY player.playerID'

    if (guiV.fName != ''):
        if (guiV.fName != None):
            name = guiV.fName.split()
            if (len(name) == 2):
                name[0] = '%' + name[0] + '%'
                name[1] = '%' + name[1] + '%'
                queryName = "player.name LIKE '{} {}'".format('%%' + name[0] + '%%', '%%' + name[1] +'%%')
            else:
                queryName = "player.name LIKE '{}'".format('%%' + name[0] + '%%')
            
            query += queryName

    if (guiV.fpos == 'Any'):
        pass
    else:
        if (queryName == None):
            queryPos = "player.playerID = isa.playerID AND isa.position = '{}'".format(guiV.fpos)
        else:
            queryPos = "AND player.playerID = isa.playerID AND isa.position = '{}'".format(guiV.fpos)
        query += queryPos

    if (guiV.fteam == 'Any'):
        pass
    else:
        if (queryName == None and queryPos == None):
            queryTeam = "player.playerID = playsfor.playerID AND playsfor.team = '{}'".format(teamABV[guiV.fteam])
        else:
            queryTeam = "AND player.playerID = playsfor.playerID AND playsfor.team = '{}'".format(teamABV[guiV.fteam])
        query += queryTeam

    print(query)

    query += endQ
    
    if (queryName == None and queryPos == None and queryTeam == None):
        refreshMainDB(mdblb, count)
    else:
        mdblb.delete(0, "end")
    
        cursor.execute(query)
        players = cursor.fetchall()
        pc = 0
        for player in players:
            pc += 1
            mdblb.insert('end', player[0] + '  |  ' + player[1])

        count.configure(text=pc)

    cursor.close()
    sys.stdout.flush()

# Change variable
def filterNameFocusOUT(p1):
    print('gui_support.filterNameFocusOUT: ' + p1.widget.get())
    guiV.fName = p1.widget.get()
    try:
        print('$' + guiV.fName + '$')
    except:
        pass

    sys.stdout.flush()

# Change variable
def filterPosFocusOUT(p1):
    print('gui_support.filterPosFocusOUT')
    guiV.fpos = p1.widget.get()
    sys.stdout.flush()

# Change variable
def filterTeamFocusOUT(p1):
    print('gui_support.filterTeamFocusOUT')
    guiV.fteam = p1.widget.get()
    sys.stdout.flush()

# Delete all database entries from all tables
# In reality, just drops all tables then reinitializes them
def clearDatabase(mdblb, count):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sqlite_master WHERE type ="table"')
    tables = cursor.fetchall()
    for x in tables:
        cursor.execute('DROP TABLE IF EXISTS ' + x[1])

    sqlCREATETABLES()
    sqlINITIALIZETABLES()
    refreshMainDB(mdblb, count)

    cursor.close()

# Populates info box data on main listbox selection
def mainDBSelected(p1, name, pos, hw, bday, college, team, pid, canvas):
    guiV.mainDBSelectTEXT = p1.widget.curselection()
    selected = p1.widget.get(guiV.mainDBSelectTEXT)
    playerID = selected.split()[0]
    guiV.mainDBSelectPiD = playerID

    print('gui_support.mainDBSelected')
    print('Selected: ' + selected)
    print('pid: ' + playerID)
    cimg = canvas.find_all()
    canvas.delete(cimg)

    cursor = conn.cursor()
    cursor.execute('SELECT player.playerID, player.name, player.hw, player.bday, player.img, isa.position, playedfor.college, playsfor.team FROM player JOIN isa ON (player.playerID = isa.playerID) JOIN playedfor ON (player.playerID = playedfor.playerid) JOIN playsfor ON (player.playerID = playsfor.playerid) WHERE player.playerID = (?)', (playerID,))
    row = cursor.fetchall()
    print(row)

    name.configure(text=row[0][1])
    pos.configure(text=row[0][5])
    hw.configure(text=row[0][2])
    bday.configure(text=row[0][3])
    college.configure(text=row[0][6])

    teamVar = list(teamABV.keys())[list(teamABV.values()).index(row[0][7])]
    team.configure(text=teamVar)
    pid.configure(text=row[0][0])

    if (row[0][4] != None):
        raw_data = urllib.request.urlopen(row[0][4]).read()
        im = Image.open(io.BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)
        canvas.create_image((65,90), image=image)
        images.append(image)

    cursor.close()
    sys.stdout.flush()

# Begins webscraping process and populates searchbox
def playerSearchBTNPress(p1, lb, count):
    print('gui_support.playerSearchBTNPress')

    lb.delete(0, "end")
    if guiV.pSearchPos == 'Any':
        possiblePlayers = stats.addPlayer(guiV.pSearchName)
    else:
        possiblePlayers = stats.addPlayer(guiV.pSearchName, guiV.pSearchPos)

    guiV.possiblePlayers = possiblePlayers

    print(possiblePlayers)

    for player in possiblePlayers:
        if player == None:
            pass
        lb.insert('end', player['name'])

    sys.stdout.flush()

# Change variable
def playerSearchNameFocusOUT(p1):
    print('gui_support.playerSearchNameFocusOUT')
    print('p search box: ' + p1.widget.get())
    guiV.pSearchName = p1.widget.get()
    sys.stdout.flush()

# Change variable
def playerSearchPosFocusOUT(p1):
    print('gui_support.playerSearchPosFocusOUT')
    print('p search box: ' + p1.widget.get())
    guiV.pSearchPos = p1.widget.get()
    sys.stdout.flush()
    
# Populates search listbox when an entry is selected
def searchLBSelected(p1, name, pos, hw, bday, college, team, pid, canvas):
    guiV.selectedSearch = p1.widget.index("active")
    print('gui_support.searchLBSelected')
    print('Selected: ' + guiV.possiblePlayers[guiV.selectedSearch]['name'])
    cimg = canvas.find_all()
    canvas.delete(cimg)

    
    print(guiV.selectedSearch)
    name.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['name'])
    pos.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['Pos'])
    hw.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['H/W'])
    bday.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['Born'])
    college.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['College'])
    team.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['Team'])
    pid.configure(text=guiV.possiblePlayers[guiV.selectedSearch]['playerID'])

    if (guiV.possiblePlayers[guiV.selectedSearch]['img'] != None):
        raw_data = urllib.request.urlopen(guiV.possiblePlayers[guiV.selectedSearch]['img']).read()
        im = Image.open(io.BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)
        canvas.create_image((45,70), image=image)
        images.append(image)

    sys.stdout.flush()

# Begins webscraping process for entire teams
def teamSearchBTNPress(p1, lb):
    print('gui_support.teamSearchBTNPress')
    lb.delete(0, "end")
    print(guiV.tSearchName + guiV.tSearchYear)
    possiblePlayers = stats.addTeam(guiV.tSearchName, guiV.tSearchYear)

    guiV.possiblePlayers = possiblePlayers

    print(possiblePlayers)

    for player in possiblePlayers:
        if player == None:
            possiblePlayers.remove(player)
            continue
        lb.insert('end', player['name'])

    sys.stdout.flush()

# Resets main database listbox to show all database entries
def refreshMainDB(mdblb, count):
    mdblb.delete(0, "end")

    cursor = conn.cursor()
    cursor.execute('SELECT playerID, name FROM player ORDER BY playerID')
    rows = cursor.fetchall()
    for row in rows:
        rowString = row[0] + '  |  ' + row[1]
        mdblb.insert('end', rowString)

    cursor.execute('SELECT COUNT(*) FROM player')
    count.configure(text=cursor.fetchone()[0])

# Change variable
def teamSearchTeamFocusOUT(p1):
    print('gui_support.teamSearchTeamFocusOUT')
    try:
        print('Team Search Name Selected: ' + guiV.tSearchName)
    except:
        print('No team search name selected')
    guiV.tSearchName = p1.widget.get()
    sys.stdout.flush()

# Change variable
def teamSearchYearFocusOUT(p1):
    print('gui_support.teamSearchYearFocusOUT')
    try:
        print('Team Search Year Selected: ' + guiV.tSearchYear)
    except:
        print('No team search year selected')
    guiV.tSearchYear = p1.widget.get()
    sys.stdout.flush()

# Add player to database and refresh main database listbox
def addPlayerToDB(p1, mdblb, count):
    try:
        print('gui_support.addPlayerToDB')
        cursor = conn.cursor()
        player = guiV.possiblePlayers[guiV.selectedSearch]

        print('Adding ' + player['name'])
        if (player['Team'].split()[-1] == 'Team'):
            player['Team'] = 'Washington'

        # Add to player table
        cursor.execute('INSERT OR IGNORE INTO player VALUES (?, ?, ?, ?, ?, ?)', (player['playerID'], player['url'], player['name'], player['H/W'], player['Born'], player['img']))

        # Add relation to isa table
        cursor.execute('INSERT OR IGNORE INTO isa VALUES (?, ?)', (player['playerID'], player['Pos']))

        # Team table
        if player['Team'] == 'F/A or Retired':
            cursor.execute('INSERT OR IGNORE INTO playsfor VALUES (?, ?)', (player['playerID'], 'FA/R'))
        else:
            playersTeam = player['Team'].split()[-1]
            cursor.execute('INSERT OR IGNORE INTO playsfor VALUES (?, ?)', (player['playerID'], teamABV[playersTeam]))

        # college
        # Because there are so many colleges, we don't initialize a list at the beginning so we insert here
        if player['College'] == None:
            cursor.execute('INSERT OR IGNORE INTO playedfor VALUES (?, ?)', (player['playerID'], 'None'))
        else:
            cursor.execute('INSERT OR IGNORE INTO college VALUES (?)', (player['College'],))
            cursor.execute('INSERT OR IGNORE INTO playedfor VALUES (?, ?)', (player['playerID'], player['College']))


        cursor.close()

        refreshMainDB(mdblb, count)

        sys.stdout.flush()
    except:
        print('Error adding player to DB')
        refreshMainDB(mdblb, count)

# Add every player in search listbox to database
def addAllToDB(p1, mdblb, count):
    try:
        print('gui_support.addAllToDB')
        cursor = conn.cursor()

        for player in guiV.possiblePlayers:
            # Add to player table
            print('Adding ' + player['name'])
            if (player['Team'].split()[-1] == 'Team'):
                player['Team'] = 'Washington'
            cursor.execute('INSERT OR IGNORE INTO player VALUES (?, ?, ?, ?, ?, ?)', (player['playerID'], player['url'], player['name'], player['H/W'], player['Born'], player['img']))

            # Add relation to isa table
            cursor.execute('INSERT OR IGNORE INTO isa VALUES (?, ?)', (player['playerID'], player['Pos']))

            # Team table
            if player['Team'] == 'F/A or Retired':
                cursor.execute('INSERT OR IGNORE INTO playsfor VALUES (?, ?)', (player['playerID'], 'FA/R'))
            else:
                playersTeam = player['Team'].split()[-1]
                cursor.execute('INSERT OR IGNORE INTO playsfor VALUES (?, ?)', (player['playerID'], teamABV[playersTeam]))

            # college
            # Because there are so many colleges, we don't initialize a list at the beginning so we insert here
            if player['College'] == None:
                cursor.execute('INSERT OR IGNORE INTO playedfor VALUES (?, ?)', (player['playerID'], 'None'))
            else:
                cursor.execute('INSERT OR IGNORE INTO college VALUES (?)', (player['College'],))
                cursor.execute('INSERT OR IGNORE INTO playedfor VALUES (?, ?)', (player['playerID'], player['College']))

        cursor.close()
        refreshMainDB(mdblb, count)

        sys.stdout.flush()
    except:
        print("Error adding all to database")
        refreshMainDB(mdblb, count)

# Export entire main database to a csv file
def exportToCSV():
    fileD = filedialog.asksaveasfilename(filetypes=[("CSV", "*.csv")])
    with open(file=fileD, mode='w', newline='') as F:
        csvWrite = csv.writer(F)

        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT player.playerID, player.refurl, player.name, player.hw, player.bday, player.img, isa.position, playedfor.college, playsfor.team FROM player INNER JOIN isa ON player.playerID = isa.playerID INNER JOIN playedfor ON player.playerID = playedfor.playerID INNER JOIN playsfor ON player.playerID = playsfor.playerID')
        csvWrite.writerows(cursor.fetchall())
        cursor.close()

# Export only filtered entries to csv file
def filterToCsvBTNPress(p1):
    fileD = filedialog.asksaveasfilename(initialdir = "/", filetypes=[("CSV", "*.csv")])
    if (fileD == '' or fileD == None):
        return

    with open(file=fileD, mode='w', newline='') as F:
        csvWrite = csv.writer(F)
        cursor = conn.cursor()
        cursor.execute(query)
        Players = []
        for x in cursor.fetchall():
            pid = x[0]
            cursor.execute('SELECT DISTINCT player.playerID, player.refurl, player.name, player.hw, player.bday, player.img, isa.position, playedfor.college, playsfor.team FROM player INNER JOIN isa ON player.playerID = isa.playerID INNER JOIN playedfor ON player.playerID = playedfor.playerID INNER JOIN playsfor ON player.playerID = playsfor.playerID WHERE player.playerID = (?)', (pid, ))
            Players.append(cursor.fetchone())
        
        for x in Players:
            print(x)

        csvWrite.writerows(Players)
        cursor.close()

# Import to main database from CSV file
def importFromCSV(mdblb, count):
    fileD = filedialog.askopenfilename(initialdir = "/", filetypes=[("CSV", "*.csv")])
    if (fileD == '' or fileD == None):
        return
    with open(file=fileD, mode='r', newline='') as F:
        csvRead = csv.reader(F)

        for row in csvRead:
            img = row[5]
            college = row[7]
            if (img == ''):
                img = None

            if (college == 'None'):
                college = None

            

            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO college VALUES (?)', (college,))
            cursor.execute('INSERT OR IGNORE INTO player VALUES (?, ?, ?, ?, ?, ?)', (row[0], row[1], row[2], row[3], row[4], img))
            cursor.execute('INSERT OR IGNORE INTO isa VALUES (?, ?)', (row[0], row[6]))
            cursor.execute('INSERT OR IGNORE INTO playsfor VALUES (?, ?)', (row[0], row[8]))
            cursor.execute('INSERT OR IGNORE INTO playedfor VALUES (?, ?)', (row[0], college))
            print("Inserting " + row[0])
    
    refreshMainDB(mdblb, count)

# Create new database
def newDB(mdblb, count):
    newDBF = filedialog.asksaveasfilename(initialdir = "/", filetypes=[('SQLite DB File', '*.db')])
    if (newDBF == '' or newDBF == None):
        return
    
    global conn
    conn = sqlite3.connect(newDBF, isolation_level=None)
    conn.execute('PRAGMA foreign_keys = ON')
    tabNum = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if (len(tabNum.fetchall()) == 0):
        print("No tables found, initializing new DB")
        sqlCREATETABLES()
        sqlINITIALIZETABLES()
    else:
        print("Tables found Found")
        
    refreshMainDB(mdblb, count)

# Load database from .db file
def loadDB(mdblb, count):
    newDBF = filedialog.askopenfilename(initialdir = "/", filetypes=[('SQLite DB File', '*.db')])
    if (newDBF == '' or newDBF == None):
        return

    global conn
    conn = sqlite3.connect(newDBF, isolation_level=None)
    conn.execute('PRAGMA foreign_keys = ON')
    refreshMainDB(mdblb, count)

# Close window 
def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

# Create all tables
def sqlCREATETABLES():
    global conn
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE player (playerID text PRIMARY KEY, refurl text, name text, hw text, bday text, img text)')
    cursor.execute('CREATE TABLE position (name text PRIMARY KEY, side text)')
    cursor.execute('CREATE TABLE college (name text PRIMARY KEY)')
    cursor.execute('CREATE TABLE team (name text, abv text PRIMARY KEY, city text)')
    cursor.execute('CREATE TABLE isa (playerID text PRIMARY KEY, position text REFERENCES position(name), FOREIGN KEY(playerID) REFERENCES player(playerID) ON DELETE CASCADE)') # FOREIGN KEY(position) REFERENCES position(name)
    cursor.execute('CREATE TABLE playsfor (playerID text PRIMARY KEY, team text, FOREIGN KEY(playerID) REFERENCES player(playerID) ON DELETE CASCADE, FOREIGN KEY(team) REFERENCES Team(abv))')
    cursor.execute('CREATE TABLE playedfor (playerID text PRIMARY KEY, college text, FOREIGN KEY(playerID) REFERENCES player(playerID) ON DELETE CASCADE, FOREIGN KEY(college) REFERENCES college(name))')
    cursor.close()

# Initialize tables with certain prewritten data
def sqlINITIALIZETABLES():
    oPos = ['QB','RB', 'HB', 'TB','FB', 'LH', 'RH', 'BB', 'B', 'WB', 'FL', 'SE', 'E', 'LE', 'WR','TE', 'OT', 'LT', 'RT', 'T','G', 'OG','C', 'OL', 'P','K','LS']
    dPos = ['DE','DT', 'NT', 'DL', 'ROLB','LOLB', 'LLB', 'RLB','LILB', 'OLB','ILB', 'MLB', 'LB', 'CB','DB','SS','FS','S']
    

    cities = ['Arizona','Atlanta','Baltimore','Buffalo','Carolina','Chicago',
            'Cincinnati','Cleveland','Dallas','Denver','Detroit','Green Bay',
            'Houston','Indianapolis','Jacksonville','Kansas City','Los Angeles',
            'Los Angeles','Miami','Minnesota','New England','New Orleans','New York',
            'New York','Oakland','Philadelphia','Pittsburgh','San Francisco','Seattle',
            'Tampa Bay','Tennessee','Washington', 'F/A or Retired' ]

    cursor = conn.cursor()

    for x in oPos:
        cursor.execute('INSERT INTO position VALUES (?,?)', (x, 0))
    
    for x in dPos:
        cursor.execute('INSERT INTO position VALUES (?,?)', (x, 1))

    for x in teamABV:
        cursor.execute('INSERT INTO team VALUES (?, ?, ?)', (x, teamABV[x], cities.pop(0)))

    noCollege = 'None'
    cursor.execute('INSERT INTO college VALUES (?)', (noCollege,))
    cursor.close()

if __name__ == '__main__':
    import gui

    tabNum = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if (len(tabNum.fetchall()) == 0):
        print("No DB file found, creating new DB")
        sqlCREATETABLES()
        sqlINITIALIZETABLES()
    else:
        print("DB Found")

    gui.vp_start_gui()




