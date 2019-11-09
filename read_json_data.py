import requests
import json
# from tqdm import tqdm
# import time

class nba_data():

    def __init__(self):
        self.get_json
        self.json = get_json()

    def get_json():
        team_names = ['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL',
                     'MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

        # get the data from nba's json
        url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
        response = requests.get(url)
        data = response.json()
        #Store the data for each game into a variable
        games = data['gs']['g']
        game_data = []

        for _,g in enumerate(games):
            game_data.append((g["stt"],_,g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))

        json_data = json.dumps(game_data, ensure_ascii=False)
        return json_data

nba_data = nba_data()
