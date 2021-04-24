from RiotAPI import RiotAPI
import csv

def get_matchResult(matchData, name):

    participantID = 0
    for participantIdentities in matchData['participantIdentities']:
        for value in participantIdentities['player'].values():
            if name == value:
                participantID = participantIdentities['participantId']
            else:
                continue

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

def write_csv(dict):
    with open('summoner_by_name', 'a') as file:
        writer = csv.writer(file)
        for key, value in dict.items():
            writer.writerow([key, value])



def main():
    apikey = 'RGAPI-21a0bebc-f5f0-4c22-80c5-cfb9103a9b4e'  # API KEY IS HERE
    api = RiotAPI(apikey)
    summoner = {}

    api = RiotAPI(apikey)
    summoner = api.get_summoner_by_name('Controleed Freak')

    # begin index starts at 0, and end index is not included for the game number. Ex. 0->5 = First 5 games (0+1->5)
    beginIndex = int(input('Enter beginIndex: '))
    endIndex = int(input('Enter endIndex: '))

    matchlist = api.get_matchlist_by_account(
        summoner['accountId'], {'beginIndex': beginIndex, 'endIndex': endIndex})

    print("Winrate (" + "Game " + str(beginIndex + 1) + " -> Game " + str(endIndex) +
          ") : " + str(round(get_winRate(matchlist, "Controleed Freak", api)))+"%")
    #a = api.get_summoner_by_name('Controleed Freak')
    print(summoner['profileIconId'])


if __name__ == "__main__":
    main()
