from dotenv import load_dotenv
import os
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
import pandas as pd
import time
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'youtube-scraper.cxuykfjq7u4s.us-west-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'pushu6789'
app.config['MYSQL_DB'] = 'youtube_scraper'
mysql = MySQL(app)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def search():
    if request.method == 'POST':
        # on the basis of search text...search on youtube
        search_text = request.form['search_text']
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
        res=render_template('index.html', results=results)
        return res
    else:
        return render_template('index.html')
@app.route('/videos',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def video_details():
    if request.method == 'POST':
        details = request.form
        channel_name = request.form['channel_name']
        cur = mysql.connection.cursor()
        sql="select * from youtuber where channel_name=%s"
        adr = (channel_name,)
        cur.execute(sql, adr)
        results = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('base.html', results=results)

@app.route('/comment',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def comment_details():
    if request.method == 'GET':

        searchTitle = request.args.get('sid')

        st=str(searchTitle)
        print(st)
        try:
            load_dotenv()
            '''MONGODB_URI = os.getenv("MONGODB_URI")
            client = pymongo.MongoClient(MONGODB_URI)
            #client = pymongo.MongoClient("mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
            db = client.test
            #print(db)
            database = client['Youtuber']
            print(database)
            collection = database["reviews"]
            #print(collection)
            # collection.insert_many(data)
            title = collection.find({'Url':st})'''
            # Connect to the MongoDB database using our connection string.
            client = MongoClient(
                'mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority')

            # Connect to the coin_markets database and the prices collection.
            db = client.get_database('Youtuber')
            db_prices = db.get_collection('reviews')
            title = db_prices.find({'Url': st})
            print(title)
            l = []
            for i in title:
                l.append(i)
            print(l)
            return render_template('results.html', title=l)  # show the results to user

        except:
            return db_prices
    else:
            return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)