import pymongo

import io
#from grpc import Channel
from selenium.common import exceptions
import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import pandas as pd
import time
import re
import requests
from flask import Flask
import mysql.connector
from mysql.connector import Error
import pymongo

def scrape(url,title_tag):
    client = pymongo.MongoClient("mongodb+srv://amitava_2112:Suman123@python.e0zfy.mongodb.net/?retryWrites=true&w=majority")
    db = client.test
    database = client['Youtuber']
    collection = database["reviews"]
    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    try:
        # Extract the elements storing the video title and
        # comment section.
        title = driver.find_element(By.XPATH, '//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element(By.XPATH, '//*[@id="comments"]')
        #views = driver.find_element(By.XPATH, '//*[@id = "count"]/ytd-video-view-count-renderer/span[1]').text
        date = driver.find_element(By.XPATH, '//*[@id="info-strings"]/yt-formatted-string').text
        channel = driver.find_element(By.XPATH, '//*[@id="text"]/a').text
        #subscribers = driver.find_element(By.XPATH, '//*[@id="owner-sub-count"]').text
        #description = driver.find_element(By.XPATH, '//*[@id="description"]/yt-formatted-string').text
    except exceptions.NoSuchElementException:
        # Note: Youtube may have changed their HTML layouts for
        # videos, so raise an error for sanity sake in case the
        # elements provided cannot be found anymore.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # Scroll into view the comment section, then allow some time
    # for everything to be loaded as necessary.
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extract the elements storing the usernames and comments.
        username_elems = driver.find_elements(By.XPATH, '//*[@id="author-text"]')
        comment_elems = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    #print("> VIDEO TITLE: " + title + "\n")
    #print("> VIEWS of Video: " + views + "\n")
    #print#("> Date: " + date + "\n")
    #print(">Channel Name: " + channel + "\n")
    #print(">Subscribers: " + subscribers + "\n")
    #print(">Description: " + description + "\n")
    mydict = {}
    for username, comment in zip(username_elems, comment_elems):
        mydict = {"Channel_name":channel,"Url":url,"Title":title_tag,"Commenter": username.text, "Review": comment.text}  # saving that detail to a dictionary
        collection.insert_one(mydict)
    driver.close()


#if __name__ == "__main__":
    #scrape("https://www.youtube.com/watch?v=WMolA7QMP5w")