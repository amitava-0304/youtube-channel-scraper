import MySQLdb
import pandas as pd
import sqlite3
df = pd.DataFrame([['Hitesh Choudhary2', 'DevOps Pro Course launch | Live classes', 15356,'https://www.youtube.com/watch?v=2fXQvy0kFakyyyy','https://i.ytimg.com/vi/2fXQvy0kFak/sddefault.jpg', '730']],columns=['channel_name', 'video_titles', 'video_views', 'video_links', 'video_thumbnail_urls','vedio_likes'])

def connection():
    conn = MySQLdb.connect(host="youtube-scraper.cxuykfjq7u4s.us-west-2.rds.amazonaws.com",
                           user = "admin",
                           passwd = "pushu6789",
                           db = "youtube_scraper")
    c = conn.cursor()
    for i, row in df.iterrows():
        sql = """INSERT IGNORE INTO youtuber(channel_name,video_titles,video_views,video_links,video_thumbnail_urls,vedio_likes) VALUES (%s, %s, %s, %s, %s, %s);"""
        c.execute(sql, tuple(row))
        conn.commit()
'''df = pd.DataFrame([['Hitesh Choudhary','DevOps Pro Course launch | Live classes',15356,'https://www.youtube.com/watch?v=2fXQvy0kFak','https://i.ytimg.com/vi/2fXQvy0kFak/sddefault.jpg','730']],columns =['channel_name','video_titles','video_views','video_links','video_thumbnail_urls','vedio_likes'])
cols = "', '".join([str(i) for i in df.columns.tolist()])
#print(df.iloc[0, :])

try:
    sqliteConnection = sqlite3.connect('youtube_scraper.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    # Insert DataFrame records one by one.
    for i in range(len(df)):
        #sql = "INSERT INTO 'youtuber' (channel_name,video_titles,video_views,video_links,video_thumbnail_urls,vedio_likes) VALUES (" + "%s,"*(len(row)-1) + "%s)"
        for i, row in df.iterrows():
            #print(tuple(row))
            #sql = "INSERT INTO `youtuber` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
            sql="""INSERT INTO youtuber
                                      (channel_name,video_titles,video_views,video_links,video_thumbnail_urls,vedio_likes) 
                                      VALUES (?, ?, ?, ?, ?);"""
            cursor.execute(sql, tuple(row))
        #cursor.execute("""INSERT INTO youtuber (channel_name,video_titles,video_views,video_links,video_thumbnail_urls,vedio_likes)""", df.iloc[i, :])
        #cursor.execute(sql, tuple(row))
        # the connection is not autocommitted by default, so we must commit to save our # changes
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()
except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")'''

#connection()