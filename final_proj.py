import json
import pandas as pd
import random
import plotly.graph_objects as go
import plotly.express as px
from flask import Flask, render_template, request, session
from flask_session.__init__ import Session

##### Loading Tree Data #####
f = open("tree.json", 'r')
tree = json.load(f)
f.close()


##### Constructing Tree Nodes #####
class Node():
    def __init__(self, left = None, right = None, data = None, name = None):
        self.left = left
        self.right = right
        self.data = data
        self.name = name

# Questions Nodes
dance = Node(data = tree[0])
dance.left = Node(data = tree[1][0])
dance.left.left = Node(data = tree[1][1][0])
dance.left.right = Node(data = tree[1][1][0])
dance.left.left.left = Node(data = tree[1][1][1][0])
dance.left.right.right = Node(data = tree[1][1][1][0])
dance.left.left.right = Node(data = tree[1][1][1][0])
dance.left.right.left = Node(data = tree[1][1][1][0])
dance.right = Node(data = tree[1][0])
dance.right.left = Node(data = tree[1][1][0])
dance.right.right = Node(data = tree[1][1][0])
dance.right.left.left = Node(data = tree[1][1][1][0])
dance.right.right.right = Node(data = tree[1][1][1][0])
dance.right.left.right = Node(data = tree[1][1][1][0])
dance.right.right.left = Node(data = tree[1][1][1][0])

# Data Nodes
dance.left.left.left.left = Node(data = tree[1][1][1][1][0])
dance.left.left.left.right = Node(data = tree[1][1][1][2][0])
dance.left.left.right.left = Node(data = tree[1][1][2][1][0])
dance.left.left.right.right = Node(data = tree[1][1][2][2][0])
dance.left.right.left.left = Node(data = tree[1][2][1][1][0])
dance.left.right.left.right = Node(data = tree[1][2][1][2][0])
dance.left.right.right.left = Node(data = tree[1][2][2][1][0])
dance.left.right.right.right = Node(data = tree[1][2][2][2][0])
dance.right.left.left.left = Node(data = tree[2][1][1][1][0])
dance.right.left.left.right = Node(data = tree[2][1][1][2][0])
dance.right.left.right.left = Node(data = tree[2][1][2][1][0])
dance.right.left.right.right = Node(data = tree[2][1][2][2][0])
dance.right.right.left.left = Node(data = tree[2][2][1][1][0])
dance.right.right.left.right = Node(data = tree[2][2][1][2][0])
dance.right.right.right.left = Node(data = tree[2][2][2][1][0])
dance.right.right.right.right = Node(data = tree[2][2][2][2][0])


##### Functions for Flask #####
def get_recommendations(q1,q2,q3,q4):
    current_node = dance  
    for i in [q1,q2,q3,q4]:
        if i == 'y':
            current_node = current_node.left
        elif i == 'n':
            current_node = current_node.right

    rec_list = []
    n = 1
    for track in random.sample(current_node.data, 10):
        if track not in rec_list:
            rec_list.append(track)
            # print(f"[{n}] {track['Track']} - {track['Artist']}")
        else:
            continue
        n += 1
    return rec_list

def get_original_data():
    f = open("Top_Tracks_Data.json", 'r')
    data = json.load(f)
    f.close()
    return data

def insertionSort(array, index):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key[index] > array[j][index]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array

def plotRadar(r_lst, theda_lst):
    df = pd.DataFrame(dict(r=r_lst,
        theta=theda_lst))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 1])))
    fig.update_traces(fill='toself')
    plot_div = fig.to_html(full_html=False)
    return plot_div


##### Setting Up Flask #####
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation')
def form_recommendation():
    return render_template('input1.html')

@app.route('/results1', methods=['POST'])
def results():
    ans1 = request.form['ans1']
    ans2 = request.form['ans2']
    ans3 = request.form['ans3']
    ans4 = request.form['ans4']
    results = get_recommendations(ans1,ans2,ans3,ans4)
    result_list = []
    for n in range(len(results)):
        result_list.append(f"[{n+1}] {results[n]['Track']} - {results[n]['Artist']}")
    session['my_var'] = results
    return render_template('results1.html', result_list = result_list, results = results)

@app.route('/plot1', methods=['POST'])
def plot():
    selected_num = int(request.form['track'])
    results = session.get('my_var', None)
    track = results[selected_num]["Track"]
    artist = results[selected_num]["Artist"]
    album = results[selected_num]["Album"]
    genre = results[selected_num]["Genre"]
    release_date = results[selected_num]["Release Date"]
    popularity = results[selected_num]["Popularity"]
    acousticness = results[selected_num]["acousticness"]
    danceability = results[selected_num]["danceability"]
    energy = results[selected_num]["energy"]
    instrumentalness = results[selected_num]["instrumentalness"]
    liveness = results[selected_num]["liveness"]
    speechiness = results[selected_num]["speechiness"]
    
    # Plotting Radar Chart
    audio_features = [acousticness, danceability, energy, instrumentalness, liveness, speechiness]
    audio_features_str = ['acousticness','danceability','energy','instrumentalness', 'liveness', 'speechiness']
    plot_div = plotRadar(audio_features, audio_features_str)
    
    return render_template('plot1.html', plot_div = plot_div, track = track, artist = artist, popularity = popularity, album = album, release_date = release_date, genre=genre)

@app.route('/tracks')
def result2():
    # Top 10 Ranking Table
    top_tracks = get_original_data()
    top10_lst = []
    n = 1
    for i in range(10):
        d = {}
        d['Rank']=n
        top_tracks[i].update(d)
        top10_lst.append(top_tracks[i])
        n += 1

    # Popularity Bars
    sorted = top10_lst[:]
    insertionSort(sorted, 'Popularity')
    track_names = []
    track_popularity = []
    for track in sorted:
        track_names.append(track['Track'])
        track_popularity.append(track['Popularity'])
    x_vals = track_names
    y_vals = track_popularity
    bars_data = go.Bar(x=x_vals, y=y_vals)
    fig = go.Figure(data=bars_data)
    fig.update_layout(height = 600)
    div1 = fig.to_html(full_html=False)

    # Average Radar
    df = pd.DataFrame.from_records(top10_lst)
    audio_features_str = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
    mean_lst = []
    for i in audio_features_str:
        mean_lst.append(df[i].mean())
    div2 = plotRadar(mean_lst, audio_features_str)

    return render_template('results2.html', top10_lst=top10_lst, sorted = sorted, plot_div1=div1, plot_div2=div2)
    

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)