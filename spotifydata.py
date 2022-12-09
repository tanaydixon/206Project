import spotipy
import spotipy.util as util
#from spotipy.oauth2 import SpotifyClientCredentials

import os
import matplotlib.pyplot as plt

import sqlite3



# username = '316qlwtjr4yhyleissfe6vis6iqi'
# # scope = 'user-read-private user-read-playback-state user-modify-playback-state'

def getSpotifyObject(username, scope):
    token = util.prompt_for_user_token(username, scope, client_id = '46282d85ebe64cfa9fc2d7de035bce0e', 
                                                            client_secret = '355ae8f3f3b14ee19a7a470d22413bdc',
                                                                redirect_uri='http://rahat.com/')
    spotify = spotipy.Spotify(auth=token)
    return spotify
def user_info(spotify):
    return spotify.current_user()

def create_playlist(spotify):
    #user_id = spotify.user_info().get('id', "None")
    top_50_usa_data = spotify.playlist_tracks('37i9dQZF1DXcBWIGoYBM5M')
   
    top_50_uk_data = spotify.playlist_tracks('153yGNYdzvyCZxzDnIzNUx')
    song_tuple_list = []

    rank_counter = 1 
    for song in top_50_usa_data['items']:
        song_id = song['track']['id']
        song_title = song['track']['name']
        song_artist = song['track']['artists'][0]['name']
        song_pop= song['track']['popularity']
        song_date = song['track']['album']['release_date']
        song_rank = rank_counter
        song_tuple_list.append((song_id, song_title, song_artist, song_rank, song_date, song_pop, "usa"))
        rank_counter += 1 

    rank_counter = 1 
    for song in top_50_uk_data['items']:
        song_id = song['track']['id']
        song_title = song['track']['name']
        song_artist = song['track']['artists'][0]['name']
        song_pop= song['track']['popularity']
        song_date = song['track']['album']['release_date']
        song_rank = rank_counter
        song_tuple_list.append((song_id, song_title, song_artist, song_rank, song_date, song_pop, "uk"))
        rank_counter += 1 
    return song_tuple_list


def join_tables(cur, conn):
    cur.execute("SELECT Hot100.song, ArtistIds.artist FROM Hot100 LEFT JOIN ArtistIds ON Hot100.artist_id = ArtistIds.artist_id")
    results = cur.fetchall()
    conn.commit()
    return results


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createDatabase(cur, conn, spotify):
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (song_id TEXT, song_title TEXT, song_artist TEXT, song_rank INTEGER, song_date TEXT, song_pop INTEGER, country_code TEXT)") 
    cur.execute("SELECT COUNT(*) FROM Spotify")
    add_25 = cur.fetchone()[0]
    for item in create_playlist(spotify)[add_25:add_25+25]:
        cur.execute("INSERT INTO Spotify (song_id, song_title, song_artist, song_rank, song_date, song_pop, country_code) VALUES (?, ?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4], item[5], item[5]))
        add_25 += 1
    conn.commit()


def main():
    spotify = getSpotifyObject("7tj4dlofb2yvuijru40p3grnp", 'playlist-modify-public')
    
    cur, conn = setUpDatabase('Billboard.db')
    createDatabase(cur, conn, spotify)
    conn.close()


if __name__ == "__main__":
    main()
