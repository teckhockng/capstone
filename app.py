import flask
import pandas as pd
import numpy as np
import datetime as DT
import requests
from tensorflow.keras.models import load_model
import json
import time
import re
# from celery import Celery

app = flask.Flask(__name__)

#Celery configuration
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

#Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

model = load_model('model.h5')

# @celery.task(bind=True)
# def get_json_data(self):
#     # get the data from nba's json
#     url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
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
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
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
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    games = data['gs']['g']
    game_data = []
    for _,g in enumerate(games):
        game_data.append((g["stt"],_,g["cl"],g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))
    json_data = json.dumps(game_data, ensure_ascii=False)
    print("Job is done!!!")
    print(json_data)
    return json_data

# API to update game data and predictions
@app.route('/get_predictions/<int:game_id>', methods=['GET'])
def get_win_percentage(game_id):
    # get the data from nba's json
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    game = data['gs']['g'][game_id]
    game_data = []
    game_status = game["stt"]
    time_remaining = game["cl"]
    time_remaining = re.findall(r'[0-9]{1,2}:[0-9]{2}',time_remaining)[0]
    visitor_score = game["v"]["s"]
    home_score = game["h"]["s"]

    if game_status == "1st Qtr":
        time_played = np.round((DT.datetime(1900,1,1,0,12) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "2nd Qtr":
        time_played = np.round((DT.datetime(1900,1,1,0,24) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "3rd Qtr":
        time_played = np.round((DT.datetime(1900,1,1,0,36) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "4th Qtr":
        time_played = np.round((DT.datetime(1900,1,1,0,48) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "OT 1":
        time_played = np.round((DT.datetime(1900,1,1,0,53) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "OT 2":
        time_played = np.round((DT.datetime(1900,1,1,0,58) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "OT 3":
        time_played = np.round((DT.datetime(1900,1,1,1,3) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "OT 4":
        time_played = np.round((DT.datetime(1900,1,1,1,8) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    elif game_status == "OT 5":
        time_played = np.round((DT.datetime(1900,1,1,1,13) - DT.datetime.strptime(time_remaining,'%M:%S')).total_seconds()/60,2)
    else:
        time_played = 48

    prediction_data = [[time_played, home_score, visitor_score]]
    home_win_percentage = np.round(model.predict(prediction_data)[0][0]*100,2)
    visitor_win_percentage = np.round(100-home_win_percentage,2)

    game_data.append((game["stt"],game["cl"],game["v"]["s"],game["h"]["s"],game["v"]["ta"],game["h"]["ta"],home_win_percentage,visitor_win_percentage))
    json_data = json.dumps(game_data, ensure_ascii=False)
    print(json_data)
    return json_data

# Prediction page
@app.route('/results/<int:game_id>')
def result(game_id):
    url = 'https://data.nba.com/data/5s/v2015/json/mobile_teams/nba/2019/scores/00_todays_scores.json'
    response = requests.get(url)
    data = response.json()
    #Store the data for each game into a variable
    game = data['gs']['g'][game_id]
    game_status = game["stt"]
    time_remaining = game["cl"]
    time_remaining = re.findall(r'[0-9]{1,2}:[0-9]{2}',time_remaining)[0]
    visitor_score = game["v"]["s"]
    home_score = game["h"]["s"]
    visitor = game["v"]["ta"]
    home = game["h"]["ta"]

    return flask.render_template('game_prediction.html', game_status=game_status, time_remaining=time_remaining,
    visitor_score=visitor_score, home_score=home_score, visitor=visitor, home=home)

# @app.route('/result', methods=['POST'])
# def result():
#     if flask.request.method == 'POST':
#         inputs = flask.request.form
#         list_tags = inputs.getlist('tags')
#         print(str(list_tags))
#         # date = str(inputs['published_date'])
#         # unix_ts = datetime.datetime.strptime(date, '%Y-%m-%d')
#         # published_date = int(unix_ts.timestamp())
#
#         data = pd.DataFrame([{
#             'description': inputs['description'],
#             'duration': inputs['duration'],
#             'languages': inputs['languages'],
#             'published_day': inputs['day'],
#             'published_month': inputs['month'],
#             'tags': str(list_tags),
#             'title': inputs['title']
#         }])
#
#         viral = pipe.predict(data)[0]
#         prob = np.round(pipe.predict_proba(data)[0][1] * 100, decimals=2)
#
#         if (viral == 1):
#             prediction = 'will be'
#         else:
#             prediction = 'will not be'
#
#         return flask.render_template("results.html", prediction=prediction, prob=prob)

if __name__ == '__main__':
    app.run(debug=True)
