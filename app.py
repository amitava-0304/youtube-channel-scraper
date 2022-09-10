import pymongo
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import pandas as pd
import time
import re
import numpy
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
        url = "https://www.youtube.com/results?search_query="+search_text.replace(' ','+')
        '''driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        time.sleep(5)

        # get channel details
        channel_section = driver.find_element(By.ID,"content-section")
        channel_details = channel_section.text.split("\n")
        channel_name = channel_details[0]
        channel_subscribers = channel_details[1].split(" ")[0]
        channel_desc = channel_details[2]
        no_of_videos = channel_details[1].split(" ")[1][12:]

        avtar = channel_section.find_element(By.XPATH,"//*[@id='avatar-section']/a")
        channel_url = avtar.get_attribute("href")
        img_section = channel_section.find_element(By.ID,"img")
        channel_avtar_url = img_section.get_attribute("src")

        driver.quit()
        reviews=[]
        mydict={"channel_name":channel_name,"channel_subscribers":channel_subscribers,"no_of_videos":no_of_videos,"channel_desc":channel_desc,"channel_avtar_url":channel_avtar_url,"channel_url":channel_url}
        reviews.append(mydict)'''
        details = request.form
        #channel_name = request.form['channel_name']
        cur = mysql.connection.cursor()
        print(search_text)
        sql = "select * from youtuber_channel where channel_name=%s"
        adr = (search_text,)
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
            client = pymongo.MongoClient(
                "mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
            db = client.test
            print(db)
            database = client['Youtuber']
            print(database)
            collection = database["reviews"]
            #print(collection)
            # collection.insert_many(data)
            title = collection.find({'Url':st})
            print(title)
            l = []
            for i in title:
                l.append(i)
            print(l)
            return render_template('results.html', title=l)  # show the results to user

        except:
            return 'something is wrong'
    else:
            return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)