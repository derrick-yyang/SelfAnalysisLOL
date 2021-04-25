from RiotAPI import RiotAPI
from RiotParser import RiotParser
import pandas as pd


def get_matchResult(matchData, name):

    participantID = 0
    for participantIdentities in matchData['participantIdentities']:
        if name == participantIdentities['player']['summonerName']:
            participantID = participantIdentities['participantId']
    return matchData['participants'][participantID-1]['stats']['win']


def get_winRate(matchList, name, api):

    numberOfMatches = len(matchList['matches'])
    numberOfWins = 0

    for i in range(numberOfMatches):
        if get_matchResult(api.get_match_by_matchid(matchList['matches'][i]['gameId']), name) == True:
            numberOfWins += 1

    if numberOfMatches != 0:
        return numberOfWins/numberOfMatches*100
    else:
        return "Matchlist empty --"


def main():
    for i in range(1):
        print(i)
    apikey = 'RGAPI-21a0bebc-f5f0-4c22-80c5-cfb9103a9b4e'  # API KEY IS HERE
    api = RiotAPI(apikey)
    summonerName = input("Enter Summoner Name:")
    summoner = api.get_summoner_by_name(summonerName)

    # begin index starts at 0, and end index is not included for the game number. Ex. 0->5 = First 5 games (0+1->5)
    beginIndex = int(input('Enter beginIndex: '))
    endIndex = int(input('Enter endIndex: '))

    matchList = api.get_matchlist_by_account(
        summoner['accountId'], {'beginIndex': beginIndex, 'endIndex': endIndex})
    # print("Winrate (" + "Game " + str(beginIndex + 1) + " -> Game " + str(endIndex) +
    #       ") : " + str(round(get_winRate(matchList, summonerName, api)))+"%")
    # a = api.get_summoner_by_name('Controleed Freak')
    print(summoner['profileIconId'])

    # add all match data into a list
    matchData = []
    for i in range(endIndex - beginIndex):
        print(i)
        matchData.append(api.get_match_by_matchid(
            matchList['matches'][i]['gameId']))

    parser = RiotParser(matchData, summonerName)
    parsedData = parser.parseData()
    print(parsedData)
    df = pd.DataFrame.from_dict(parsedData)

    for i in range(len(parsedData["Summoner Name"])):
        print(i)
        rowLabelIndex = df.index[i]
        df = df.rename(index={rowLabelIndex: "Match " + str(i + 1)})

    df.to_csv('data.csv', mode='a')


if __name__ == "__main__":
    main()
