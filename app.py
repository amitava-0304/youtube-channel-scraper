from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request,jsonify
from flask import Flask, render_template,request,redirect,url_for
from flask_cors import CORS,cross_origin
import requests
import pandas as pd
import time
import certifi
from flask_mysqldb import MySQL
import os
import aws_S3_videos
import setup
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'youtube-scraper.cxuykfjq7u4s.us-west-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'pushu6789'
app.config['MYSQL_DB'] = 'youtube_scraper'
mysql = MySQL(app)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    setup.configure()
    return render_template("index.html")
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def search():
    if request.method == 'POST':
        # on the basis of search text...search on youtube
        search_text = request.form['search_text']
        no = request.form['no']
        print(no)
        details = request.form
        cur = mysql.connection.cursor()
        print(search_text)
        sql = "select * from youtuber_channel where channel_name like %s"
        adr = (search_text+"%",)
        cur.execute(sql, adr)
        results = cur.fetchall()
        print(results)
        mysql.connection.commit()
        cur.close()
        res=render_template('index.html', results=results,no=no)
        return res
    else:
        return render_template('index.html')
@app.route('/videos',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def video_details():
    if request.method == 'POST':
        details = request.form
        channel_name = request.form['channel_name']
        no = int(request.form['no'])
        print(channel_name)
        print(no)
        cur = mysql.connection.cursor()
        sql="select * from youtuber where channel_name=%s order by video_titles desc LIMIT %s"
        adr = (channel_name,no)
        cur.execute(sql, adr)
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('base.html', results=results)

@app.route('/comment',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def comment_details():
    l = []
    mongo_url=setup.get_mongodb_url()
    client = MongoClient(mongo_url)
    db = client.Youtuber
    db_reviews = db.reviews
    if request.method == 'GET':

        searchTitle = request.args.get('sid')

        st=str(searchTitle)
        print(st)
        try:
            # Connect to the MongoDB database using our connection string.
            title = db_reviews.find({'Url': st})
            print(title)
            #l = []
            for i in title:
                l.append(i)
            print(l)
            return render_template('results.html', title=l)  # show the results to user

        except:
            return l
    else:
            return render_template('index.html')

@app.route('/download',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def download():
    if request.method == 'GET':
         ul=request.args.get('sid')
         id=ul[32:len(ul)]
         url = f"https://www.youtube.com/watch?v={id}"
         link = aws_S3_videos.handle_videos(url)
    return f"<a href={link}>Download the Video from this URL............</a>"

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run()