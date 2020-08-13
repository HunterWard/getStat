# variables.py
#
# Contains class which holds data for gui backend
# If GUI was implemented differently using tracing of entry boxes
# this class wouldn't be needed.  
# Hunter Ward
# 7/6/20
class guiVars:
    pSearchName = None
    pSearchPos = None

    tSearchName = None
    tSearchYear = None

    selectedSearch = None

    mainDBSelectTEXT = None
    mainDBSelectPiD = None
    
    possiblePlayers = None

    #Filter Vars
    fName = None
    fpos = 'Any'
    fteam = 'Any'
    fDiv = 'Any'

    def __init__(self):
        pass