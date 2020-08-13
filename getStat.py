from bs4 import BeautifulSoup as Soup
import utils


class getStats:

    def __init__(self):
        pass
        
    # addPlayer - add statistics to list
    def addPlayer(self, name, pos=None):
        player = utils.genUrlAndProfile(name, pos)
        return player

    # addTeam
    # Webscrapes for entire team
    def addTeam(self, name, year):
        teamURL = utils.genTeamUrl(name, year)
        playerLinks = utils.collectTeamLinks(teamURL)
        returnList = []
        for link in playerLinks:
            if (link == None):
                pass
            else:
                newPlayer = utils.genPlayerProfile(link)
                if (newPlayer == None):
                    pass
                returnList.append(newPlayer)

        return returnList