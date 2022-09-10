from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import download
from sqlalchemy import create_engine
# import required packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import pandas as pd
import time
import re
import comments
import numpy
import data_import
import image_downloader
import proj

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("home.html")
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def search():
    if request.method == 'POST':
        # on the basis of search text...search on youtube
        search_text = request.form['search_text']
        #searchString = request.form['content'].replace(" ", "+")
        #flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        #uClient = uReq(flipkart_url)
        url = "https://www.youtube.com/results?search_query="+search_text.replace(' ','+')
        #url = "https://www.youtube.com/results?search_query=" + searchString
        #print(search_text)
        print(url)

        # put that searching url into chrome driver with the help of selenium
        driver = webdriver.Chrome()
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

        # display channel details
        print("Channel name : ",channel_name)
        print("Channel subscribers : ",channel_subscribers)
        print("Number of videos : ",no_of_videos)
        print("Channel Description : ",channel_desc)

        avtar = channel_section.find_element(By.XPATH,"//*[@id='avatar-section']/a")
        channel_url = avtar.get_attribute("href")
        img_section = channel_section.find_element(By.ID,"img")
        channel_avtar_url = img_section.get_attribute("src")

        print("channal_url : ",channel_url)
        print("channel_avtar_url :",channel_avtar_url)

        driver.quit()
        reviews=[]

        mydict={"channel_name":channel_name,"channel_subscribers":channel_subscribers,"no_of_videos":no_of_videos,"channel_desc":channel_desc,"channel_avtar_url":channel_avtar_url,"channel_url":channel_url}
        reviews.append(mydict)
        res=render_template('home.html', reviews=reviews)
        return res
    else:
        return render_template('home.html')
@app.route('/videos',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def top_videos():
    if request.method == 'POST':
        channel_avtar_url = request.form['channel_avtar_url']
        channel_name = request.form['channel_name']
        channel_subscribers = request.form['channel_subscribers']
        no_of_videos = request.form['no_of_videos']
        channel_desc = request.form['channel_desc']
        channel_url = request.form['channel_url']

        print("channel_avtar_url_inside_top_videos : ",channel_avtar_url)
        print("channel_name_inside_top_videos : ",channel_name)
        print("channel_subscribers_inside_top_videos : ",channel_subscribers)
        print("no_of_videos_inside_top_videos : ",no_of_videos)
        print("channel_desc_inside_top_videos : ",channel_desc)
        print("channel_url_inside_top_videos : ",channel_url)

        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(channel_url)
        time.sleep(5)
        channel_section = driver.find_element(By.ID, "tabsContainer")
        channel_details = channel_section.text.split("\n")
        channel_section.find_element(By.XPATH,"//*[@id='tabsContent']/tp-yt-paper-tab[2]/div").click()
        time.sleep(5)
        #no_of_videos='50'
        if ',' not in no_of_videos:
            no_of_videos = int(no_of_videos)
        else:
            no_of_videos = int(no_of_videos[:no_of_videos.index(',')])*1000 + int(no_of_videos[no_of_videos.index(',')+1:])

        count = 1
        while True:
            driver.execute_script("window.scrollBy(0,1000)","")
            time.sleep(3)
            video_sections = driver.find_elements(By.ID,"video-title")
            print(len(video_sections))
            print(count)
            count = count+1


            if len(video_sections) >= no_of_videos-4:
                break

        video_links = []

        for i in video_sections:
            video_links.append(i.get_attribute("href"))

        print(len(video_links))

        video_titles = []
        video_lengths = []
        video_descs = []
        video_views = []
        video_ratings = []
        video_age_restricted = []
        video_thumbnail_urls = []
        video_likes = []
        flag = 1
        for i in video_links[0:5]:
            #driver1 = webdriver.Chrome()

            # Navigates to the URL, maximizes the current window, and
            # then suspends execution for (at least) 5 seconds (this
            # gives time for the page to load).
            #driver1.get(i)
            yt = YouTube(i)
            video_titles.append(yt.title)
            #video_lengths.append(yt.length)
            video_descs.append(yt.description)
            video_views.append(yt.views)
            video_thumbnail_urls.append(yt.thumbnail_url)
            #video_likes.append(driver.find_element(By.XPATH,'//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a').text)
        print(flag)
        flag = flag + 1
        for i in video_links[0:5]:
            c=comments.scrape(i)
            for j in c:
                video_likes.append(j)
        #for i in video_links[0:2]:


        video_likes=list(numpy.concatenate(video_likes).flat)
        df = pd.DataFrame(list(zip(video_titles,video_views,video_links,video_thumbnail_urls,video_likes)),columns =['video_titles','video_views','video_links','video_thumbnail_urls','vedio_likes'])
        #final = df.sort_values(by=['video_views','video_ratings'],ascending=False).head(10)
        df.insert(loc=0, column='channel_name', value=channel_name)
        #mydb = database.create_database_connection()
        data_import.insert_query(df)
        count = 1
        for i in video_thumbnail_urls:
            image_downloader.download_image(i, (channel_name+str(count)),channel_name)
            count += 1
        for i,j in zip(video_links[0:5],video_titles[0:5]):
            proj.scrape(i,j)
        download.downloader(video_links[0:5], channel_name)
    #reviews = []
    #data={"channel_name":channel_name,"channel_subscribers":channel_subscribers,"no_of_videos":no_of_videos,"channel_desc":channel_desc,"channel_avtar_url":channel_avtar_url}
    #a.append(data)
    #res = render_template('home.html',data=final)
    #mydict = {"video_titles": video_titles, "video_views": video_views,  "video_links": video_links,"channel_avtar_url": channel_avtar_url}  # saving that detail to a dictionary
    #data1={"data": final}
    #print(data1)
    #reviews.append(mydict)  # appending the comments to the review list
    driver.close()
    return render_template('home.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    #return render_template('home.html', reviews=reviews)
    #return res

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)