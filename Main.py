from RiotAPI import RiotAPI
from RiotParser import RiotParser
import time

def main():

    apikey = 'RGAPI-72d0e930-a00d-4814-9b6f-071c988f6b71'  # API KEY IS HERE
    api = RiotAPI(apikey)

    # User input starts here:
    summonerName = 'Controleed Freak'

    # begin index starts at 0, and end index is not included for the game number. Ex. 0->5 = First 5 games (0+1->5)

    beginCount = 0
    endCount = 1
    matchDataList = []
    num = 10
    for i in range(num):
        matchDataList.append(api.get_matchDataList_by_account(summonerName, beginCount * 98, endCount *98))
        beginCount += 1
        endCount += 1
        if i != num - 1:
            time.sleep(121)

    parser = RiotParser(matchDataList[0], summonerName)
    parsedDf = parser.parseData()

    for i in range (1, num):
        parser = RiotParser(matchDataList[i], summonerName)
        newParsedDf = parser.parseData()
        result = parsedDf.append(newParsedDf)
        parsedDf = result

    parsedDf.to_csv('Controleed Freak.csv', mode='w')

if __name__ == "__main__":
    main()