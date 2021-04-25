
# Given the match data from get_match_by_matchid from RiotAPI
# Returns a panda Dataframe with the following column information (in this order):
#   - Summoner name
#   - Game Duration
#   - Match Result
#   - Champion
#   - Creep Score
#   - Gold Total
#   - Champion Level
#   - Vision Score

class RiotParser(object):

    def __init__(self, matchDataList, name):
        self.matchDataList = matchDataList
        self.summonerName = name

    # Parses desired data (refer to above) from a list of matchData into a dictionary
    def parseData(self):
        dataList = self.matchDataList
        parsedData = {'Summoner Name': [],
                      'Game Duration': [],
                      'Match Result': [],
                      'Champion ID': [],
                      'Creep Score': [],
                      'Gold Earned': [],
                      'Champion Level': [],
                      'Vision Score': []
                      }

        for i in range(len(dataList)):
            if dataList[i]['mapId'] == 11 and dataList[i]['gameMode'] == 'CLASSIC':
                participantID = 0
                for participantIdentities in dataList[i]['participantIdentities']:
                    if self.summonerName == participantIdentities['player']['summonerName']:
                        participantID = participantIdentities['participantId']
                mr = ''
                if dataList[i]['participants'][participantID - 1]['stats']['win'] == True:
                    mr = 'Victory'
                else:
                    mr = 'Defeat'
                # Creating the dictionary
                parsedData['Summoner Name'].append(self.summonerName)
                parsedData['Game Duration'].append(dataList[i]['gameDuration'])
                parsedData['Match Result'].append(mr)
                parsedData['Champion ID'].append(dataList[i]['participants'][participantID - 1]['championId'])
                parsedData['Creep Score'].append(dataList[i]['participants'][participantID - 1]['stats']['totalMinionsKilled'])
                parsedData['Gold Earned'].append(dataList[i]['participants'][participantID - 1]['stats']['goldEarned'])
                parsedData['Champion Level'].append(dataList[i]['participants'][participantID - 1]['stats']['champLevel'])
                parsedData['Vision Score'].append(dataList[i]['participants'][participantID - 1]['stats']['visionScore'])

        return parsedData
