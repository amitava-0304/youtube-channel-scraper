from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import expected_conditions as EC
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time

def scrape(url):
    driver = webdriver.Chrome()
    likes = []
    com=[]
    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)
        likes.append(driver.find_element(By.XPATH,'//*[@id="top-level-buttons-computed"]/ytd-toggle-button-renderer[1]/a').text)
        com.append(driver.find_element(By.XPATH,'//*[@id="count"]').text)

    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)
    for i in com:
        #print(">Likes: " + i + "\n")
        yield likes
        driver.close()
    #return likes

#if __name__ == "__main__":
    #scrape(["https://www.youtube.com/watch?v=2fXQvy0kFak&t=333s", "https://www.youtube.com/watch?v=rp56yKfIkmo"])