from sqlalchemy import create_engine
import pymysql
import pandas as pd
import MySQLdb
def insert_query(query):
    '''conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="youtube_scraper")'''
    conn = MySQLdb.connect(host="youtube-scraper.cxuykfjq7u4s.us-west-2.rds.amazonaws.com",
                           user="admin",
                           passwd="pushu6789",
                           db="youtube_scraper")
    c = conn.cursor()

    try:
      for i, row in query.iterrows():
          sql = """INSERT IGNORE INTO youtuber(channel_name,video_titles,video_views,video_links,video_thumbnail_urls,vedio_likes) VALUES (%s, %s, %s, %s, %s, %s);"""
          c.execute(sql, tuple(row))
          conn.commit()

    except ValueError as v:
        print(v)

    except Exception as e:
        print(e)

    else:
         print("data inserted successfully......")

    finally:
         conn.close()
