import RiotConsts as Consts
import requests

class RiotAPI(object):

    def __init__(self, api_key, region=Consts.REGIONS['north_america_platform_1']):
        self.api_key = api_key
        self.region = region

    def _request (self, api_url, params={}):

        args = {'api_key': self.api_key}

        for key, value in params.items():
            if key not in args:
                args[key]=value
            
        response = requests.get (
            Consts.URL['base'].format(
                proxy=self.region,
                url=api_url
            ),
            params=args
        )
        print(response.url)
        return response.json()


#Request functions from RiotAPI link
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
        return self._request (api_url, params)

    def get_match_by_matchid(self, match):
        
        api_url = Consts.URL['matches_by_matchID'].format(
            version=Consts.API_VERSIONS['match'],
            matchID=match
        )

        return self._request (api_url)

