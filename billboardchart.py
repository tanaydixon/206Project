
import billboard
import sqlite3
import os


def get_billboard_data():
    chart = billboard.ChartData('hot-100')
#pulling data from billboard top 100
    song_title_list = []
    artist_name_list =[]
    weeks_on_chart_list =[]
    song_rank_list = []
    for i in range(len(chart)):  
        song = chart[i]
        
        song_rank = song.rank
        song_title = song.title
        
        artist_name = song.artist
        weeks_on_chart = song.weeks
        artist_name_list.append(artist_name)
        song_rank_list.append(song_rank)
        song_title_list.append(song_title)
        weeks_on_chart_list.append(weeks_on_chart)
   #creating categories for songs based on num of weeks on the chart 
    songCategory = []
    for song in weeks_on_chart_list:
        if song < 5:
            songCat = 1
        elif song < 10:
            songCat = 2
        elif song < 15:
            songCat = 3
        elif song < 20:
            songCat = 4
        else:
            songCat = 5
        songCategory.append(songCat)
   
    return song_title_list, artist_name_list, song_rank_list,weeks_on_chart_list, songCategory
    
        
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_Billbaord_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS BillBoardSongs (song TEXT, artist TEXT , rank INTEGER UNIQUE, weeks_id INTEGER)") 
    song, artist, ranking, weeksOnTop100, songCategory = get_billboard_data()
    cur.execute("CREATE TABLE IF NOT EXISTS WeeksID (songCategory INTEGER, weeks TEXT)") 
    cur.execute('SELECT* FROM BillBoardSongs JOIN WeeksID ON BillBoardSongs.weeks_id = WeeksID.songCategory')
    cur.execute('SELECT max (rank) from BillBoardSongs')
    startIndex = cur.fetchone()[0]
    if startIndex == None:
        startIndex = 0
    
    #print(startIndex)
    for item in range(startIndex, startIndex + 25):
        if startIndex == 100:
            pass
        else:

            cur.execute("INSERT INTO BillBoardSongs (song, artist, rank, weeks_id) VALUES (?, ?, ?, ?)", (song[item], artist[item], ranking[item], songCategory[item]))
    conn.commit()
    
def create_Weeks_id_Table(cur, conn):
    stringWeeks = ['less than 5 weeks', 'less than 10 weeks', 'less than 15 weeks', 'less than 20 weeks', 'more than 20 weeks']
    #song, artist, ranking, weeksOnTop100, songCategory = getBillBoardLink()
    cur.execute('SELECT max (songCategory) from WeeksID')
    maxNum = cur.fetchone()[0]
    if maxNum == 5:
        pass
    else:
        for item in range(5):
            cur.execute("INSERT INTO WeeksID (songCategory, weeks) VALUES (?, ?)", (item+1, stringWeeks[item]))
    conn.commit()

    #pass

def main():
    get_billboard_data()
    cur, conn = setUpDatabase('BillBoard.db')
    create_Billbaord_table(cur, conn)
    create_Weeks_id_Table(cur, conn)

if __name__ == "__main__":
    main()
  





   

    
    
    
        
  


