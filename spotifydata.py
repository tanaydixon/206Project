import spotipy
import spotipy.util as util
import os
import matplotlib.pyplot as plt
import sqlite3


def getSpotifyObject(username, scope):
    token = util.prompt_for_user_token(username, scope, client_id = '46282d85ebe64cfa9fc2d7de035bce0e', 
                                                            client_secret = '355ae8f3f3b14ee19a7a470d22413bdc',
                                                                redirect_uri='http://rahat.com/')
    spotify = spotipy.Spotify(auth=token)
    return spotify

#creating spotify playlists
def create_playlist(spotify):
    top_50_usa_data = spotify.playlist_tracks('37i9dQZEVXbLRQDuF5jeBp')
    top_50_uk_data = spotify.playlist_tracks('1QM1qz09ZzsAPiXphF1l4S')
    song_tuple_list = []
    rank_counter = 1 
#categorizing information for US songs
    for song in top_50_usa_data['items']:
        song_id = song['track']['id']
        song_title = song['track']['name']
        song_artist = song['track']['artists'][0]['name']
        song_pop= song['track']['popularity']
        song_date = song['track']['album']['release_date']
        song_rank = rank_counter
        song_tuple_list.append((song_id, song_title, song_artist, song_rank, song_date, song_pop, "usa"))
        rank_counter += 1 
#categorizing information for UK songs
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

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
# def create_artist_table(cur, conn, spotify):
#     cur.execute("CREATE TABLE IF NOT EXISTS Artist ( artist TEXT, artist_id INTEGER UNIQUE)") 
#     cur.execute("SELECT COUNT(*) FROM Artist")
#     add_25 = cur.fetchone()[0]
#     for item in create_playlist(spotify)[add_25:add_25+25]:
#         cur.execute("INSERT INTO Artist ( artist, artist_id) VALUES (?, ?)", (item[2], item+1))
#         add_25 += 1
#     conn.commit()

#creating data base by pulling 25 songs at a time - need to be ran 4 times 
def create_spotify_table(cur, conn, spotify):
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify (song_id TEXT, song TEXT, artist TEXT, song_rank INTEGER , song_date TEXT, song_pop INTEGER, country_code TEXT)") 
    cur.execute("SELECT COUNT(*) FROM Spotify")
    add_25 = cur.fetchone()[0]
    for item in create_playlist(spotify)[add_25:add_25+25]:
        cur.execute("INSERT INTO Spotify (song_id, song, artist, song_rank, song_date, song_pop, country_code) VALUES (?, ?, ?, ?, ?, ?, ?)", (item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
        add_25 += 1
    conn.commit()


def main():
    spotify = getSpotifyObject("7tj4dlofb2yvuijru40p3grnp", 'playlist-modify-public')
    cur, conn = setUpDatabase('Billboard.db')
    create_spotify_table(cur, conn, spotify)
    conn.close()

if __name__ == "__main__":
    main()
