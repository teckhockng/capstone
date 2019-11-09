import requests
import json
from tqdm import tqdm
import time
import urllib

team_names = ['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL',
             'MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

for n in tqdm(team_names):
    logo = urllib.request.URLopener()
    team_logo_url = f'https://stats.nba.com/media/img/teams/logos/season/2019-20/{n}_logo.svg'
    logo.retrieve(team_logo_url, f"/home/nthock/Documents/capstone/static/images/{n}_logo.svg")
    time.sleep(1)
