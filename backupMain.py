from RiotAPI import RiotAPI
from RiotParser import RiotParser
import constants as Consts
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
# This file is treated as a back up for Main on jupyter Notebook

# create_csv() generates a csv file with parsed data for 686 games of the user indicated by
#   summonerName.
def create_csv(api, summonerName):

    count = 0
    matchDataList = []
    # represents number of 98 list of game data requests for this player (7*98 = 686 games will be parsed)
    num = 7
    for i in range(num):
        matchDataList.append(api.get_matchDataList_by_account(
            summonerName, count * 98, (count + 1) * 98))
        count += 1

        if i != num - 1:
            time.sleep(121)

    parser = RiotParser(summonerName)
    parsedDf = parser.parseData(matchDataList[0])

    for i in range(1, num):
        parser = RiotParser(summonerName)
        newParsedDf = parser.parseData(matchDataList[i],)
        result = parsedDf.append(newParsedDf)
        parsedDf = result

    print(parsedDf)
    parsedDf.to_csv(summonerName + '.csv', mode='w')

    print('File Successfully Created: ' + summonerName + '.csv')
    time.sleep(121)


def get_winRate_list(df, parser):

    # The list is represented as follows:
    # winRates[0] : 0 - 10 mins
    # winRates[1] : 10 - 20 mins
    # winRates[2] : 20 - 30 mins
    # winRates[3] : 30 - 40 mins
    # winRates[4] : 40+ mins
    winRates = []

    for i in range(2, 8):
        # winrate calculated by wins/total games within a certain timeframe
        wins = df.loc[(df[parser.GAME_DURATION] >= 60 * (i * 5)) &
                       (df[parser.GAME_DURATION] < 60 * ((i + 1) * 5)) &
                       (df[parser.MATCH_RESULT] == 'Victory')].shape[0]
        totalGames = df.loc[(df[parser.GAME_DURATION] >= 60 * (i * 5)) &
                            (df[parser.GAME_DURATION] < 60 * ((i + 1) * 5))].shape[0]

        winrate = int(wins / totalGames * 100)

        winRates.append(winrate)

    # This is for winrate 40+ mins
    wins = df.loc[(df[parser.GAME_DURATION] >= 60 * 40) &
                  (df[parser.MATCH_RESULT] == 'Victory')].shape[0]
    totalGames = df.loc[(df[parser.GAME_DURATION] >= 60 * 40)].shape[0]

    winrate = int(wins / totalGames * 100)
    winRates.append(winrate)

    return winRates


def main():

    apikey = Consts.API_KEY['apikey']
    api = RiotAPI(apikey)

    df1 = pd.read_csv('Controleed Freak.csv')
    df2 = pd.read_csv('Ender Dragon 3.csv')
    df3 = pd.read_csv('cyrs7.csv')
    df4 = pd.read_csv('Belox.csv')

    # Axis Labels:
    # x-axis: matchtime
    # y-axis: players
    matchtime = ['10 - 15', '15 - 20', '20 - 25',
                 '25 - 30', '30 - 35', '35 - 40',
                 '40+']
    players = ['Controleed Freak', 'Ender Dragon 3', 'cyrs7', 'Belox']

    parser = RiotParser('Controleed Freak')
    winrateArray = np.array([get_winRate_list(df1, parser),
                            get_winRate_list(df2, parser),
                            get_winRate_list(df3, parser),
                            get_winRate_list(df4, parser)])
    
    # Heat map Specifics:
    fig, ax = plt.subplots(figsize=(12,4))
    sb.heatmap(winrateArray, xticklabels=matchtime, yticklabels=players, annot=True, ax=ax)

    plt.xlabel("Game Duration (mins)")
    plt.ylabel("Players")

    ax.set_title("% Winrate by Game Duration (300+ Games)")
    fig.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()
