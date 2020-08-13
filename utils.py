# utils.py
#
# Contains helper functions for getStat.py
# Hunter Ward
# 7/6/20

from bs4 import BeautifulSoup as Soup
import requests
from requests_html import HTMLSession

# formatPlayerName
# Preprocesses name for URL
def formatPlayerName(name):
    nameFL = name.split()

    # Format name for URL
    # Take out periods in names like TJ
    for x in range(2):
        nameFL[x] = nameFL[x].replace('.', '')
    
    # Add x to end of name less than 4 chars
    while len(nameFL[1]) < 4:
        nameFL[1] += 'x'

    return nameFL

# getNewUrl
# Given a preprocessed name and iteration number, creates URL
def getNewPlayerUrl(name,num):
    return ('https://www.pro-football-reference.com/players/' +
            name[1][0] +
            '/' +
            name[1][:4] +
            name[0][:2] +
            str(num).zfill(2) +
            '.htm'
            )

# parsePlayerInfo
# From lists of scraped data, creates dictionary of basic player info
def parsePlayerInfo(playerData, collegeInfo, url, photo):
    try:
        profile = {}
        profile['name'] = ' '.join(playerData[0])

        pos = playerData[1][1].split('-')[0]
        pos = pos.split('/')[0]
        pos = pos.split(',')[0]

        if (pos == 'NT'):
            pos = 'DT'
        if (pos == 'DB'):
            pos = 'CB'
        if (pos == 'RILB'):
            pos = 'MLB'
        if (pos == 'RG' or pos == 'LG'):
            pos = 'G'
        if (pos == 'EDGE'):
            pos = 'OLB'
        if (pos == 'PR'):
            pos = 'WR'

        profile['Pos'] = pos
        profile['H/W'] = ' '.join(playerData[2][:2])

        # Order of scraped data different if player is not currently on a team
        if (playerData[3][0] == 'Team:'):
            profile['Team'] = ' '.join(playerData[3][1:])
            profile['Born'] = ' '.join(playerData[4][1:4])
            if (collegeInfo != None):
                profile['College'] = collegeInfo[3].getText()
            else:
                profile['College'] = None
        else:
            profile['Team'] = 'F/A or Retired'
            profile['Born'] = ' '.join(playerData[3][1:4])
            if (collegeInfo != None):
                profile['College'] = collegeInfo[2].getText()
            else:
                profile['College'] = None

        profile['url'] = url

        if photo:
            profile['img'] = photo
        else:
            profile['img'] = None

        
        profile['playerID'] = genPlayerID(url)

        return profile
    except:
        return None

# genPlayerID
# Gets unique ID from URL
def genPlayerID(url):
    urlSplit = url.split('/')
    return urlSplit[-1].split('.')[0]

# genUrlAndProfile
# Given a player name, finds all players that fit the information
# If position is given, only returns players that fit that position
def genUrlAndProfile(nameF, pos):
    possible = []
    num = 0

    name = formatPlayerName(nameF) # Get the formatted name for the URL

    num = 0
    abnormalURL = False
    while (True): 
        url = getNewPlayerUrl(name, num)
        
        # Increment end of URL number
        num += 1

        # Get html and parse
        htm = requests.get(url)
        page = Soup(htm.text, "html.parser")

        # If Page not found, we've iterated through all possible players
        # Some players not found in regular incremented list have URL num of 20
        if (page.find(text="Page Not Found (404 error)")):
            if (len(possible) == 0 and abnormalURL == False):
                num = 20
                abnormalURL = True
                continue
            else:
                break

        # Grab div filled with player info and find the <p>'s
        playerInfo = page.find('div', itemtype="https://schema.org/Person")
        info = playerInfo.find_all('p')

        if (info == None):
            print("ERROR FINDING PAGE")

        # Colleges can be multiple words so it's best to take the text from the link to the college
        if (playerInfo.find(text="College")):
            collegeInfo = playerInfo.find_all('a')
            if playerInfo.find(text="Died:"): # If player is deceased, death date and place are added
                del collegeInfo[:2]
        else:
            collegeInfo = None

        # Get photo
        images = page.find_all('div', {"class": "media-item"})
        photo = None
        if images != []: # If image tag is found (Some players have no picture)
            photo = images[0].find_all('img')[0]['src']
            
        # Create list for players data
        playerData = []
        for x in info: # For every <p> strip the text, split it and store
            playerData.append(x.text.strip().split())

        if (pos != None):
            if (playerData[1][1] != pos): 
                continue # if this player isn't the correct position, skip him

        profile = parsePlayerInfo(playerData, collegeInfo, url, photo)
        if profile == None:
            continue

        # Add to list of possible players
        possible.append(profile)

    #TODO THIS CHOICE STUFF HAS TO GO INTO GUI SOMEHOW

    return possible

    
    #return possible[pick]

# genPlayerProfile
# Given specific player URL, creates profile dictionary
def genPlayerProfile(url):
    # Get html and parase
    htm = requests.get(url)
    page = Soup(htm.text, "html.parser")

    # If Page not found, we've iterated through all possible players
    if (page.find(text="Page Not Found (404 error)")):
        print('URL NOT VALID')
        return None

    # Grab div filled with player info and find the <p>'s
    playerInfo = page.find('div', itemtype="https://schema.org/Person")
    info = playerInfo.find_all('p')

    # Colleges can be multiple words so it's best to take the text from the link to the college
    if (playerInfo.find(text="College")):
        collegeInfo = playerInfo.find_all('a')
        if playerInfo.find(text="Died:"): # If player is deceased, death date and place are added
            del collegeInfo[:2]
    else:
        collegeInfo = None

    # Get photo
    images = page.find_all('div', {"class": "media-item"})
    photo = None
    if images != []: # If image tag is found (Some players have no picture)
        photo = images[0].find_all('img')[0]['src']
        
    # Create list for players data
    playerData = []
    for x in info: # For every <p> strip the text, split it and store
        playerData.append(x.text.strip().split())

    profile = parsePlayerInfo(playerData, collegeInfo, url, photo)

    return profile

# genTeamUrl
# Given a team and a year returns link to the roster page
def genTeamUrl(Team, year):
    baseURL = 'https://www.pro-football-reference.com/teams/'

    # TODO this info will probably be put into a database
    teamABV = {'CARDINALS': 'crd', 'FALCONS': 'atl',
                'RAVENS': 'rav', 'BILLS': 'buf',
                'PANTHERS': 'car', 'BEARS': 'chi',
                'BENGALS': 'cin', 'BROWNS': 'cle',
                'COWBOYS': 'dal', 'BRONCOS': 'den',
                'LIONS': 'det', 'PACKERS': 'gnb',
                'TEXANS': 'htx', 'COLTS': 'clt',
                'JAGUARS': 'jax', 'CHIEFS': 'kan',
                'CHARGERS': 'sdg', 'RAMS': 'ram',
                'DOLPHINS': 'mia', 'VIKINGS': 'min',
                'PATRIOTS': 'nwe', 'SAINTS': 'nor',
                'GIANTS': 'nyg', 'JETS': 'nyj',
                'RAIDERS': 'rai', 'EAGLES': 'phi',
                'STEELERS': 'pit', '49ERS': 'sfo',
                'SEAHAWKS': 'sea', 'BUCCANEERS': 'tam',
                'TITANS': 'oti', 'WASHINGTON': 'was'}

    return (baseURL +
            teamABV[Team.upper()] +
            '/' +
            str(year) +
            '_roster.htm')

# colleectTeamLinks
# Football reference populates full roster table with javascript
# Must use requests-html to get the 
def collectTeamLinks(url):
    # Initialize 
    links = []
    session = HTMLSession()
    getTable = session.get(url)
    getTable.html.render()

    # Find specific table of full roster
    table = getTable.html.find('#games_played_team')

    # In that table, just find the datacell that the player link is in
    rows = table[0].find("td[data-stat^='player']")
    
    # Last row is empty and error will happen if it isn't deleted
    del rows[-1]

    # For each player, add their link to list of links
    for player in rows:
        # The links set should have just one element
        links.append(player.absolute_links.pop()) 

    return links
