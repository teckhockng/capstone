from gazpacho import get, Soup
import time
from tqdm import tqdm
import pandas as pd
import numpy as np
import re
import datetime as DT

def get_pbp_links(url):
    html = get(url)
    soup = Soup(html)
    data = soup.find('td', {'data-stat': 'date_game'})
    links = [l.find('a') for l in data]
    pbp_links = ["https://www.basketball-reference.com" + l.attrs['href'].replace('scores/','scores/pbp/') for l in links]
    return pbp_links

def get_table_data(url):
    html = get(url)
    soup = Soup(html)
    table = soup.find('table', {'id': 'pbp'})
    table_data = table.find('td', {'class': 'center'})
    scores = [t.text for t in table_data]
    rows = table.find('tr',strict=True)
    times = []
    for i in rows:
        try:
            time = i.find('td', mode='first')
            times.append(time.text)
        except (IndexError, TypeError) as e:
            pass
    return scores, times

def time_played(times,scores):
    q1 = DT.datetime(1900,1,1,0,12)
    q2 = DT.datetime(1900,1,1,0,24)
    q3 = DT.datetime(1900,1,1,0,36)
    q4 = DT.datetime(1900,1,1,0,48)
    ot1 = DT.datetime(1900,1,1,0,53)
    ot2 = DT.datetime(1900,1,1,0,58)
    ot3 = DT.datetime(1900,1,1,1,3)
    ot4 = DT.datetime(1900,1,1,1,8)
    ot5 = DT.datetime(1900,1,1,1,13)

    second_quart_counter = 0
    third_quart_counter = 0
    fourth_quart_counter = 0
    ot_counter = 0
    time_played = []

    for t,s in zip(times,scores):
        t = DT.datetime.strptime(t, '%M:%S')
        if 'Start of 2nd quarter' in s:
            second_quart_counter += 1
        elif 'Start of 3rd quarter' in s:
            third_quart_counter += 1
        elif 'Start of 4th quarter' in s:
            fourth_quart_counter += 1
        elif ('Start' in s) & ('overtime' in s):
            ot_counter += 1
        elif 'End of 2nd quarter' in s:
            second_quart_counter -= 1
        elif 'End of 3rd quarter' in s:
            third_quart_counter -= 1
        elif 'End of 4th quarter' in s:
            fourth_quart_counter -= 1

        if second_quart_counter == 1:
            t = (q2-t).total_seconds()/60
            time_played.append(t)
        elif third_quart_counter == 1:
            t = (q3-t).total_seconds()/60
            time_played.append(t)
        elif fourth_quart_counter == 1:
            t = (q4-t).total_seconds()/60
            time_played.append(t)
        elif ot_counter == 1:
            t = (ot1-t).total_seconds()/60
            time_played.append(t)
        elif ot_counter == 2:
            t = (ot2-t).total_seconds()/60
            time_played.append(t)
        elif ot_counter == 3:
            t = (ot3-t).total_seconds()/60
            time_played.append(t)
        elif ot_counter == 4:
            t = (ot4-t).total_seconds()/60
            time_played.append(t)
        elif ot_counter == 5:
            t = (ot5-t).total_seconds()/60
            time_played.append(t)
        else:
            t = (q1-t).total_seconds()/60
            time_played.append(t)
    return time_played

def strip_score(score):
    home = []
    away = []
    for s in score:
        h = re.findall(r'[0-9]{1,3}$',s)[0]
        a = re.findall(r'^[0-9]{1,3}',s)[0]
        home.append(h)
        away.append(a)
    return home, away

def get_data(url):
    scores, times = get_table_data(url)

    df = pd.DataFrame({
    'time': times,
    'score': scores
    })

    df['time'] = df['time'].apply(lambda x:re.findall(r'[0-9]{1,2}:[0-9]{2}',x)[0])

    df['time'] = time_played(df['time'],df['score'])

    #remove duplicates
    df.drop_duplicates(inplace=True)

    # remove indicator of start/end of quarter
    df = df[df['score'].str.contains('-')]

    home, away = strip_score(df['score'])
    df['home'] = home
    df['away'] = away

    df.drop('score',axis=1,inplace=True)
    df['home'] = df['home'].astype(int)
    df['away'] = df['away'].astype(int)

    home_win = df['home'].iloc[-1] > df['away'].iloc[-1]
    df['home_win'] = [home_win] * len(df['home'])

    return df

# Base url for season 2017-2018
season_17_18_base_url = "https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2018&year_max=2018&is_range=N&game_num_type=team&order_by=date_game"
# Base url for season 2018-2019
season_18_19_base_url = "https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=2019&year_max=2019&is_range=N&game_num_type=team&order_by=date_game"

# Get 2018-2019 season game links
# New list to store links to play by play data
pbp_links_17_18 = get_pbp_links(season_17_18_base_url)

# loop through season 17_18 games and save play by play(pbp) game urls into season_17_18_url
# change url offset
for _ in tqdm(range(100, 2624, 100)):
    offset = _
    season_17_18_url = f"https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2018&year_max=2018&team_id=&opp_id=&is_range=N&is_playoffs=&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=date_game&order_by_asc=&offset={offset}"
    links = get_pbp_links(season_17_18_url)
    pbp_links_17_18.extend(links)
    time.sleep(1)

pbp_links_17_18 = np.unique(pbp_links_17_18)

# Get 2018-2019 season game links
pbp_links_18_19 = get_pbp_links(season_18_19_base_url)

# loop through season 18_19 games
# change url offset
for _ in tqdm(range(100, 2624, 100)):
    offset = _
    season_18_19_url = f"https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&player=&match=game&lg_id=NBA&year_min=2019&year_max=2019&team_id=&opp_id=&is_range=N&is_playoffs=&round_id=&best_of=&team_seed=&opp_seed=&team_seed_cmp=eq&opp_seed_cmp=eq&game_num_type=team&game_num_min=&game_num_max=&game_month=&game_location=&game_result=&is_overtime=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&order_by=date_game&order_by_asc=&offset={offset}"
    links = get_pbp_links(season_18_19_url)
    pbp_links_18_19.extend(links)
    time.sleep(1)

pbp_links_18_19 = np.unique(pbp_links_18_19)

# Define table for 17-18 data
df_17_18 = pd.DataFrame({
    'time':[] ,
    'home':[] ,
    'away':[],
    'home_win':[]
})


# Loop through the links in 17-18 season games and add all data into df_17_18
for l in tqdm(pbp_links_17_18):
    try:
        data = get_data(l)
        df_17_18 = df_17_18.append(data)
        time.sleep(1)
    except ValueError:
        pass

# Define table for 18-19 data
df_18_19 = pd.DataFrame({
    'time': [],
    'home': [],
    'away': [],
    'home_win':[]
})

# Loop through the links in 18-19 season games and add all data into df_18_19
for l in tqdm(pbp_links_18_19):
    try:
        data = get_data(l)
        df_18_19 = df_18_19.append(data)
        time.sleep(1)
    except ValueError:
        pass

# Export 17-18 season game data to csv
df_17_18.to_csv('/home/nthock/Documents/capstone/data/season_17_18.csv', index=False)

# Export 18-19 season game data to to_csv
df_18_19.to_csv('/home/nthock/Documents/capstone/data/season_18_19.csv', index=False)
