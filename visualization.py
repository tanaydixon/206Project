import json
import requests
import os
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def set_connection(db_file):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+db_file)
        # print('connected')
    except:
        print('not connected')
    return conn


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
def viz(data):
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
            weeks ='5 '
        elif weeks == 2:
            weeks = '10 ' 
        elif weeks == 3:
            weeks = '15 ' 
        elif weeks == 4:
            weeks = '20'
        else:
            weeks = 'more than 20'
        newList.append(weeks)
    xposition = np.arange(len(newList))
    plt.bar(xposition, numOfSongs)
    plt.xticks(xposition, newList)
    plt.xlabel('The Numbers of Weeks on The Top 100')
    plt.ylabel('Number of Songs')
    plt.title('Number of Songs vs Time on The Chart')
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
    plt.bar(xposition, numbOfSongs, color = 'purple' )
    plt.xticks(xposition, pop_on_chart)
    plt.xlabel('Rating of Popularity on Spotify Top 100')
    plt.ylabel('Number of Songs')
    plt.title('Average Amount of Popularity on Spotify Top 100')
    plt.show()

def write_calculations(data):
    f = open('billboard.txt', 'w' , encoding = 'utf-8')
    f.write(json.dumps(data))


def write_calculations(data):
    f = open('spotify_cal.txt', 'w' , encoding = 'utf-8')
    f.write(json.dumps(data))

#runs all of the code 
def main():
    conn = set_connection('BillBoard.db')
    data = get_weeks_popularity(conn)
    viz(data)
    spot_data = get_song_pop(conn)
    spotify_viz_chart(spot_data)
    write_calculations(data)
    write_calculations(spot_data)

    
    
main()