from RiotAPI import RiotAPI
from RiotParser import RiotParser
import RiotConsts as Consts
import time

# This file is treated as a back up for Main on jupyter Notebook

# create_csv() generates a csv file with parsed data for 686 games of the user indicated by
#   summonerName.
def create_csv(api, summonerName):

    count = 0
    matchDataList = []
    num = 7 # represents number of 98 list of game data requests for this player (7*98 = 686 games will be parsed)
    for i in range(num):
        matchDataList.append(api.get_matchDataList_by_account(summonerName, count * 98, (count + 1) * 98))
        count += 1

        if i != num - 1:
            time.sleep(121)

    parser = RiotParser(matchDataList[0], summonerName)
    parsedDf = parser.parseData()

    for i in range (1, num):
        parser = RiotParser(matchDataList[i], summonerName)
        newParsedDf = parser.parseData()
        result = parsedDf.append(newParsedDf)
        parsedDf = result

    print(parsedDf)
    parsedDf.to_csv(summonerName + '.csv', mode='w')

    print('File Successfully Created: ' + summonerName + '.csv')
    time.sleep(121)


def main():

    apikey = Consts.API_KEY['apikey']
    api = RiotAPI(apikey)

    summonerName = 'Controleed Freak'

if __name__ == "__main__":
    main()