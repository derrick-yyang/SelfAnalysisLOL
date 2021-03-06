import constants as Consts
import requests

# This class is responsible for making API Calls/Requests from RiotAPI
# Website: https://developer.riotgames.com/

class RiotAPI(object):

    def __init__(self, api_key, region=Consts.REGIONS['north_america_platform_1']):
        self.api_key = api_key
        self.region = region

    # function returns json response body from URL (and params)
    def _request(self, api_url, params={}):

        args = {'api_key': self.api_key}

        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            Consts.URL['base'].format(
                proxy=self.region,
                url=api_url
            ),
            params=args
        )
        return response.json()

    # request function for match-V5 (temporarily unused until they update api)
    def _requestV5(self, api_url, params={}):

        args = {'api_key': self.api_key}

        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            Consts.URL['base'].format(
                proxy='americas',
                url=api_url
            ),
            params=args
        )
        return response.json()

    # Request functions from RiotAPI URL
    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
        )
        return self._request(api_url)

    def get_matchlist_by_account(self, AccountID, params={}):

        api_url = Consts.URL['matchlist_by_accountID'].format(
            version=Consts.API_VERSIONS['match'],
            accountID=AccountID
        )
        return self._request(api_url, params)

    def get_match_by_matchid(self, matchId):

        api_url = Consts.URL['matches_by_matchID'].format(
            version=Consts.API_VERSIONS['match'],
            matchID=matchId
        )
        return self._request(api_url)

    # get_matchDataList_by_account() returns a list of matchData (using get_match_by_match_id) from 
    #   games indicated by beginIndex and endIndex
    # Note: the number of games is inclusive in the beginIndex but not endIndex 
    #       Ex. 0->5 = First 5 games (0+1->5)
    def get_matchDataList_by_account(self, name, beginIndex, endIndex):

        # Generate summoner and matchList data
        summoner = self.get_summoner_by_name(name)
        matchList = self.get_matchlist_by_account(
            summoner['accountId'], {'beginIndex': beginIndex, 'endIndex': endIndex})

        # add all match data into a list
        matchDataList = []
        for i in range(endIndex - beginIndex):
            matchDataList.append(self.get_match_by_matchid(
                matchList['matches'][i]['gameId']))

        return matchDataList
