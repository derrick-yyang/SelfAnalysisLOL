# SelfAnalysisLOL

backupMain.py contains the execution of the code to generate heatmap from existing .csv files
* To query your own data, you must generate your own API Key and put it in RiotConsts.py under API_KEY


The RiotAPI class is responsible for making API Calls/Requests from RiotAPI
Website: https://developer.riotgames.com/

## The RiotParser class does the following:
Given the match data from get_match_by_matchid from RiotAPI
Returns a panda Dataframe with the following column information (in this order):
  - Summoner name
  - Game Duration
  - Match Result
  - Champion
  - Creep Score
  - Gold Total
  - Champion Level
  - Vision Score

## getSummoners.ipynb 
- Shows the code execution of this projects Data Retrieval Process
- Retrieves Data from the Following Summoners:
    - Controleed Freak
    - Ender Dragon 3
    - cyrs7
    - Belox
    - TF Blade
    - Adrian Riven

## graphSummonerData.ipynb 
- Shows the code execution/heat map of the data collected
- Shows the Heat Map relationship for Winrate of the Summoners with respect to Game Duration

**All Documentation can be found in the classes**

## To see the final product of this project, open graphSummonerData.ipynb