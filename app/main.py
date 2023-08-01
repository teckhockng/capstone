import flask
import pandas as pd
import numpy as np
import datetime as DT
import requests
from tensorflow.keras.models import load_model
import json
import time
import re
import pickle
# from celery import Celery

app = flask.Flask(__name__)

#Celery configuration
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# model = pickle.load(open("logreg.pkl", "rb"))
model = load_model('model/model.h5')

# @celery.task(bind=True)
# def get_json_data(self):
#     # get the data from nba's json
#     url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2020/scores/00_todays_scores.json'
#     response = requests.get(url)
#     data = response.json()
#     #Store the data for each game into a variable
#     games = data['gs']['g']
#     game_data = []
#
#     for _,g in enumerate(games):
#         game_data.append((g["stt"],_,g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))
#
#     json_data = json.dumps(game_data, ensure_ascii=False)
#     print("Job is done!!!")
#     print(json_data)
#     time.sleep(5)
#     return json_data



@app.route('/')
def home():

    team_names = ['ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL',
                 'MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS']

    # get the data from nba's json
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2022/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    games = data['gs']['g']
    game_data = []

    for _,g in enumerate(games):
        game_data.append((g["stt"],_,g["cl"],g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))

    # json_data = get_json_data.apply_async()
    # json_data = celery.AsyncResult(task_id)
    # print(json_data.get())

    return flask.render_template('index.html', game_data=game_data)

# API to change home page live
@app.route('/get_data', methods=['GET'])
def get_json_data():
    # get the data from nba's json
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2020/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    games = data['gs']['g']
    game_data = []
    for _,g in enumerate(games):
        game_data.append((g["stt"],_,g["cl"],g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))
    json_data = json.dumps(game_data, ensure_ascii=False)
    print(json_data)
    return json_data

# API to update game data and predictions
@app.route('/get_predictions/<int:game_id>', methods=['GET'])
def get_win_percentage(game_id):
    # get the data from nba's json
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2020/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    game = data['gs']['g'][game_id]
    game_data = []
    game_status = game["stt"]
    time_remaining = game["cl"]

    if game["cl"] is None:
        time_remaining = "00:00"
    else:
        time_remaining = re.findall(r'[0-9]{1,2}:[0-9]{2}',time_remaining)[0]
    visitor_score = int(game["v"]["s"])
    home_score = int(game["h"]["s"])

    if "1st Qtr" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,0,12) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "2nd Qtr" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,0,24) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "3rd Qtr" in game_status :
        time_played = np.round((DT.datetime(1900,1,1,0,36) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "4th Qtr" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,0,48) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "1st OT" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,0,53) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "2nd OT" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,0,58) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "3rd OT" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,1,3) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "4th OT" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,1,8) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif "5th OT" in game_status:
        time_played = np.round((DT.datetime(1900,1,1,1,13) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "Halftime":
        time_played = np.round((DT.datetime(1900,1,1,0,24) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    else:
        time_played = 0

    # prediction_data = [time_played, home_score, visitor_score]
    # home_win_percentage = np.round(model.predict_proba([prediction_data])[0][0]*100,2)
    prediction_data = [[time_played, int(home_score), int(visitor_score)]]
    print(prediction_data)
    home_win_percentage = np.round(model.predict(prediction_data)[0][0]*100,2)
    visitor_win_percentage = np.round(100-home_win_percentage,2)

    minutes_played = re.findall(r'^[0-9]{1,3}',str(time_played))[0]
    seconds_played = np.round((time_played - float(minutes_played))*60)
    seconds_played = re.findall(r'^[0-9]{1,2}',str(minutes_played))[0]
    total_time_played = minutes_played+ ":" + seconds_played

    game_data.append((game["stt"],game["cl"],game["v"]["s"],game["h"]["s"],game["v"]["ta"],game["h"]["ta"],time_played,home_win_percentage,visitor_win_percentage))
    json_data = json.dumps(game_data, ensure_ascii=False)
    print(json_data)
    return json_data

# Prediction page
@app.route('/results/<int:game_id>')
def result(game_id):
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2020/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    game = data['gs']['g'][game_id]
    game_status = game["stt"]
    time_remaining = game["cl"]
    if time_remaining is None:
        time_remaining = "None"
    else:
        time_remaining = re.findall(r'[0-9]{1,2}:[0-9]{2}',time_remaining)[0]
    visitor_score = game["v"]["s"]
    home_score = game["h"]["s"]
    visitor = game["v"]["ta"]
    home = game["h"]["ta"]
    game_data = []

    games = data['gs']['g']
    for _,g in enumerate(games):
        game_data.append((g["stt"],_,g["cl"],g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))

    return flask.render_template('game_prediction.html', game_id=game_id, game_status=game_status, time_remaining=time_remaining,
    visitor_score=visitor_score, home_score=home_score, visitor=visitor, home=home, game_data=game_data)

# Demo page
@app.route('/demo')
def demo():
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2020/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    games = data['gs']['g']
    game = data['gs']['g'][0]
    game_status = game["stt"]
    time_remaining = game["cl"]
    if time_remaining is None:
        time_remaining = "None"
    else:
        time_remaining = re.findall(r'[0-9]{1,2}:[0-9]{2}',time_remaining)[0]
    visitor_score = game["v"]["s"]
    home_score = game["h"]["s"]
    visitor = game["v"]["ta"]
    home = game["h"]["ta"]
    game_data = []
    for _,g in enumerate(games):
        game_data.append((g["stt"],_,g["cl"],g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))
    return flask.render_template('demo.html', game_data=game_data, game_status=game_status, time_remaining=time_remaining, visitor_score=visitor_score, home_score=home_score, visitor=visitor,
    home=home)

@app.route('/get_demo_results', methods=['GET'])
def get_demo_results():
    if flask.request.method == 'GET':
        inputs = flask.request.args
        time_played = inputs.get('time_played')
        home_score = inputs.get('home_score')
        visitor_score = inputs.get('visitor_score')
        game_data = []
        if ":" not in time_played:
                time_played = (DT.datetime.strptime(time_played,'%M')- DT.datetime(1900,1,1,0,0)).total_seconds()/60
        else:
            time_played = (DT.datetime.strptime(time_played,'%M:%S')- DT.datetime(1900,1,1,0,0)).total_seconds()/60
        # prediction_data = [time_played, int(home_score), int(visitor_score)]
        # home_win_percentage = np.round(model.predict_proba([prediction_data])[0][0]*100,2)
        prediction_data = [[time_played, int(home_score), int(visitor_score)]]
        home_win_percentage = np.round(model.predict(prediction_data)[0][0]*100,2)
        visitor_win_percentage = np.round(100-home_win_percentage,2)
        game_data.append((time_played, home_win_percentage,visitor_win_percentage))
        json_data = json.dumps(game_data, ensure_ascii=False)
        return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
