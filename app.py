import flask
import pandas as pd
import numpy as np
import datetime as DT
import requests
from tensorflow.keras.models import load_model
import json
from read_json_data import nba_data

app = flask.Flask(__name__)

model = load_model('model.h5')
# data = [[47,93,97]]
# model.predict(data)

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
        game_data.append((g["stt"],_,g["v"]["s"],g["h"]["s"],g["v"]["ta"],g["h"]["ta"]))

    json_data = json.dumps(game_data, ensure_ascii=False)

    return flask.render_template('index.html', game_data=game_data, json_data=json_data)

@app.route('/result', methods=['POST'])
def result():
    if flask.request.method == 'POST':
        inputs = flask.request.form
        list_tags = inputs.getlist('tags')
        print(str(list_tags))
        # date = str(inputs['published_date'])
        # unix_ts = datetime.datetime.strptime(date, '%Y-%m-%d')
        # published_date = int(unix_ts.timestamp())

        data = pd.DataFrame([{
            'description': inputs['description'],
            'duration': inputs['duration'],
            'languages': inputs['languages'],
            'published_day': inputs['day'],
            'published_month': inputs['month'],
            'tags': str(list_tags),
            'title': inputs['title']
        }])

        viral = pipe.predict(data)[0]
        prob = np.round(pipe.predict_proba(data)[0][1] * 100, decimals=2)

        if (viral == 1):
            prediction = 'will be'
        else:
            prediction = 'will not be'

        return flask.render_template("results.html", prediction=prediction, prob=prob)

if __name__ == '__main__':
    app.run(debug=True)
