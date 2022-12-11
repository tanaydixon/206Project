import json

import os
import spotipy
import sqlite3
# import spotifydata as sp
import matplotlib.pyplot as plt
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

SPOTIPY_CLIENT_ID = '46282d85ebe64cfa9fc2d7de035bce0e'
SPOTIPY_CLIENT_SECRET= '355ae8f3f3b14ee19a7a470d22413bdc'
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def set_connection(db_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_file)
        # print('connected')
    except:
        print('not connected')
    return conn



    
def get_features(track_id):
    track_features_x = sp.audio_features(track_id)
    dfx = pd.DataFrame(track_features_x, index=[0])
    dfx_features = dfx.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
    return dfx_features

def feature_plot2(features1,features2):
    #Import Libraries for Feature plot
    
    
    labels= list(features1)[:]
    stats= features1.mean().tolist()
    stats2 = features2.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    stats2 =np.concatenate((stats2,[stats2[0]])) 
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (18,18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "USA_Song_1", color= 'blue')
    ax.fill(angles, stats, alpha=0.25, facecolor='blue')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)

    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="gray", size=12)
    plt.ylim(0,1)

    ax.plot(angles, stats2, 'o-', linewidth=2, label = "UK_Top_1", color = 'm')
    ax.fill(angles, stats2, alpha=0.25, facecolor='m' )
    ax.set_title("Comparison of the audio features of Uk Top-1 spotify song and USA top-1 song")
    ax.grid(True)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    plt.show() 
def feature_plot_billboard_Top_2(features1,features2):
    #Import Libraries for Feature plot
    
    
    labels= list(features1)[:]
    stats= features1.mean().tolist()
    stats2 = features2.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    stats2 =np.concatenate((stats2,[stats2[0]])) 
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (18,18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "Song_1", color= 'blue')
    ax.fill(angles, stats, alpha=0.25, facecolor='blue')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)

    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
    plt.ylim(0,1)

    ax.plot(angles, stats2, 'o-', linewidth=2, label = "Song_2", color = 'm')
    ax.fill(angles, stats2, alpha=0.25, facecolor='m' )
    ax.set_title("Audio Features of Top Two Billboard Songs")
    ax.grid(True)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))
    plt.show()
# get the number of weeks that songs typically spend on the charts for billboard
def get_weeks_popularity(conn):
    cur = conn.cursor()
    weeks = cur.execute('SELECT weeks_id FROM BillBoardSongs').fetchall()

    weeks_list = []
    for weekID in weeks:
        weeks_list.append(weekID)
    week_dict = {}
    for num in weeks_list:
        if num in week_dict:
            week_dict[num] += 1
        else:
            week_dict[num] = 1
   
    return week_dict


# make visualization for billboard top 100 
def viz_billboard(data):
    weeksOnChart = []
    numOfSongs = []
    dataSorted = sorted(data.items(),key = lambda x:x[0])
    for i in dataSorted:
        weeksOnChart.append(i[0])
        numOfSongs.append(i[1])
    #print(weeksOnChart)
    newList = []
    for weeks in weeksOnChart:
        weeks = weeks[0]
        if weeks == 1:
            weeks ='less than 5 weeks'
        elif weeks == 2:
            weeks = 'less than 10 weeks' 
        elif weeks == 3:
            weeks = 'less than 15 weeks' 
        elif weeks == 4:
            weeks = 'less than 20 weeks'
        else:
            weeks = 'more than 20 weeks'
        newList.append(weeks)
    fig = plt.figure(figsize =(10, 7))
    xposition = np.arange(len(newList))
    plt.bar(xposition, numOfSongs, color = 'teal')
    plt.xticks(xposition, newList)
    plt.xlabel('The Numbers of Weeks on The Top 100')
    plt.ylabel('Number of Songs')
    plt.title('Average Amount of Time Spent on Billboard Top 100')
    plt.show()



def viz_billboard_pie(data):
    weeksOnChart = []
    numOfSongs = []
    
    dataSorted = sorted(data.items(),key = lambda x:x[0])
   
    for i in dataSorted:
        weeksOnChart.append(i[0])
        numOfSongs.append(i[1])
   
   
    
    weeks = ['less than 5 weeks','less than 10 weeks', 'less than 15 weeks', 'less than 20 weeks', 'more than 20 weeks' ]
   
    fig = plt.figure(figsize =(10, 7))

    plt.pie(numOfSongs, labels = weeks, autopct= '%1.1f%%')

    plt.title('Average Number of Weeks On  Spent on Billboard Top 100')
    plt.show()


#make dictionary for spotify visual
def get_song_pop(conn):
    cur = conn.cursor()
    popularity = cur.execute('SELECT song_pop FROM Spotify').fetchall()
    song_pop_list = []
    for pop in popularity:
        song_pop_list.append(pop[0])
    song_pop_dict = {}
    for pop in song_pop_list:
        if pop > 90:
            pop = 'above 90% popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
        elif pop < 90 and pop >= 80:
            pop = '89-80% popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
        elif pop < 80 and pop >= 70:
            pop = '79-70% popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
        elif pop < 70 and pop >= 60:
            pop = '69-60% popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
        elif pop < 60 and pop >=50:
            pop = '59-50% popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
        else:
            pop = '50% & lower popularity'
            if pop in song_pop_dict:
                song_pop_dict[pop] += 1
            else:
                song_pop_dict[pop] = 1
    
    return song_pop_dict


#makes visualization for spotify top 100 charts 
def spotify_viz_chart(spot_data):
    pop_on_chart = []
    numbOfSongs = []
    dataSorted = sorted(spot_data.items(),key = lambda x:x[0])
   
    for i in dataSorted:
        pop_on_chart.append(i[0])
        numbOfSongs.append(i[1])
    xposition = np.arange(len(pop_on_chart))
    fig = plt.figure(figsize =(10, 7))
    plt.bar(xposition, numbOfSongs, color = 'purple' )
    plt.xticks(xposition, pop_on_chart)
    plt.xlabel('Rating of Popularity on Spotify Top 100')
    plt.ylabel('Number of Songs')
    plt.title('Average Amount of Popularity on Spotify Top 100')
    plt.show()
def join_tables(cur, conn):
    cur.execute("SELECT song_id FROM Spotify INNER JOIN BillBoardSongs ON Spotify.song = BillBoardSongs.song LIMIT 2")
    results = cur.fetchall()
    conn.commit()
    
    return results
    
def write_calculations(data):
    f = open('billboard.txt', 'w' , encoding = 'utf-8')
    f.write(json.dumps(data))






def top_songs_featurs():
    conn = set_connection('BillBoard.db')
    cur = conn.cursor()
    spotify_id = join_tables(cur, conn)
    
    song_1_id= spotify_id[0]
    song_2_id = spotify_id[1]

    feature_1 = get_features(song_1_id)
    featur_2 = get_features(song_2_id)

   

    compar_vis = feature_plot2(feature_1, featur_2)
    return compar_vis
    

def main():
    conn = set_connection('BillBoard.db')
    cur2 = conn.cursor()
   
    data = get_weeks_popularity(conn)
    viz_billboard(data)
    viz_billboard_pie(data)
    spot_data = get_song_pop(conn)
    spotify_viz_chart(spot_data)

   
    usa_top_1_id  = cur2.execute('SELECT song_id  FROM Spotify WHERE country_code = "usa" AND song_rank = 1').fetchone()
    
  
    uk_top_1_id  = cur2.execute('SELECT song_id  FROM Spotify WHERE country_code = "uk" AND song_rank = 1').fetchone()
    
    usa_1_features = get_features(usa_top_1_id)
    uk_1_features = get_features(uk_top_1_id)
    feature_plot_billboard_Top_2(usa_1_features, uk_1_features)

    write_calculations(spot_data)
    
    top_songs_featurs()
    get_weeks_popularity(conn)
    

main()