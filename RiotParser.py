# This class does the following:

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

# TODO2:
# find winrate
# get heat map

# TODO3 (stretch goals):
# color/scale the heatmap properly (40-60 instead of 0-100)
# adjust how big the map is (not ugly)

import pandas as pd

class RiotParser(object):

    SUMMONER_NAME = 'Summoner Name'
    GAME_DURATION = 'Game Duration'
    MATCH_RESULT = 'Match Result'
    CHAMPION_ID = 'Champion ID'
    CREEP_SCORE = 'Creep Score'
    GOLD_EARNED = 'Gold Earned'
    CHAMPION_LEVEL = 'Champion Level'
    VISION_SCORE = 'Vision Score'

    def __init__(self, matchDataList, name):
        self.matchDataList = matchDataList
        self.summonerName = name

    # Parses desired data (refer to above) from a list of matchData into a dictionary
    def parseData(self):

        # add all match data into a list
        dataList = self.matchDataList
        parsedData = {self.SUMMONER_NAME: [],
                      self.GAME_DURATION: [],
                      self.MATCH_RESULT: [],
                      self.CHAMPION_ID: [],
                      self.CREEP_SCORE: [],
                      self.GOLD_EARNED: [],
                      self.CHAMPION_LEVEL: [],
                      self.VISION_SCORE: []
                      }

        for i in range(len(dataList)):
            if 'mapId' in dataList[i].keys() and dataList[i]['mapId'] == 11 and dataList[i]['gameMode'] == 'CLASSIC':
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
                parsedData[self.SUMMONER_NAME].append(self.summonerName)
                parsedData[self.GAME_DURATION].append(
                    dataList[i]['gameDuration'])
                parsedData[self.MATCH_RESULT].append(mr)
                parsedData[self.CHAMPION_ID].append(
                    dataList[i]['participants'][participantID - 1]['championId'])
                parsedData[self.CREEP_SCORE].append(
                    dataList[i]['participants'][participantID - 1]['stats']['totalMinionsKilled'])
                parsedData[self.GOLD_EARNED].append(
                    dataList[i]['participants'][participantID - 1]['stats']['goldEarned'])
                parsedData[self.CHAMPION_LEVEL].append(
                    dataList[i]['participants'][participantID - 1]['stats']['champLevel'])
                parsedData[self.VISION_SCORE].append(
                    dataList[i]['participants'][participantID - 1]['stats']['visionScore'])

        df = pd.DataFrame.from_dict(parsedData)
        for i in range(len(parsedData["Summoner Name"])):
            rowLabelIndex = df.index[i]
            df = df.rename(index={rowLabelIndex: "Match " + str(i + 1)})

        return df
