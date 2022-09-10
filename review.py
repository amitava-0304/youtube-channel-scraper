dic = {}
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import pandas as pd
import time
import re
import csv
import io
#from grpc import Channel
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
import pandas as pd
from mysql_database import database
def scrape(url):
    """
    Extracts the comments from the Youtube video given by the URL.

    Args:
        url (str): The URL to the Youtube video

    Raises:
        selenium.common.exceptions.NoSuchElementException:
        When certain elements to look for cannot be found
    """

    # Note: Download and replace argument with path to the driver executable.
    # Simply download the executable and move it into the webdrivers folder.
    # driver= webdriver.Chrome('./webdrivers/chromedriver')
    driver = webdriver.Chrome()

    # Navigates to the URL, maximizes the current window, and
    # then suspends execution for (at least) 5 seconds (this
    # gives time for the page to load).

    # driver.get(url)
    # driver.maximize_window()
    # time.sleep(3)
    likes = []
    try:
        # Extract the elements storing the video title and
        # comment section.

            driver.get(url)
            driver.maximize_window()
            time.sleep(3)
            #title = driver.find_element(By.XPATH, '//*[@id="container"]/h1/yt-formatted-string').text
            comment_section = driver.find_element(By.XPATH, '//*[@id="comments"]')
            #views = driver.find_element(By.XPATH, '//*[@id = "count"]/ytd-video-view-count-renderer/span[1]').text
            #date = driver.find_element(By.XPATH, '//*[@id="info-strings"]/yt-formatted-string').text
            #channel = driver.find_element(By.XPATH, '//*[@id="text"]/a').text
            #subscribers = driver.find_element(By.XPATH, '//*[@id="owner-sub-count"]').text
            #description = driver.find_element(By.XPATH, '//*[@id="description"]/yt-formatted-string').text
            likes.append(driver.find_element(By.XPATH,
                                             '//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a').text)
        # total=driver.find_element(By.XPATH,'//*[@id="count"]/yt-formatted-string/span[1]').text

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
        time.sleep(5)

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


    for i in likes:
        print(">Likes: " + i + "\n")
    # print(">Likes: " + total + "\n")
    # for username, comment in zip(username_elems, comment_elems):
    # print(username.text, comment.text)
    # dic[username.text]=comment.text

    # for i in dic:
    # print(i)
    print(len(dic))
    driver.close()
    return likes

#if __name__ == "__main__":
    #scrape(["https://www.youtube.com/watch?v=2fXQvy0kFak&t=333s", "https://www.youtube.com/watch?v=rp56yKfIkmo"])