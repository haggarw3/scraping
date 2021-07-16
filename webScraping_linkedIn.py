from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests
import re
from bs4 import BeautifulSoup, ResultSet
import pandas as pd
from datetime import date, datetime
import time
import os


driver = webdriver.Firefox(executable_path='/Users/himanshuaggarwal/PycharmProjects/pythonProject/geckodriver')
# driver.manage().window().maximize()

jobs = ['data analysis', 'data analyst', 'data analysis junior', 'business analyst', 'junior analyst',
        'data science junior']


# for each job define the function to scrape
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
driver.find_element_by_id('username').send_keys(Keys.COMMAND + "a")
driver.find_element_by_id('username').send_keys(Keys.DELETE)
time.sleep(2)
driver.find_elements_by_id('username')[0].send_keys('himanshu.aggarwal@ironhack.com')
time.sleep(3)
# print("username successful")
driver.find_element_by_id('password').send_keys(Keys.COMMAND + "a")
driver.find_element_by_id('password').send_keys(Keys.DELETE)
time.sleep(2)
driver.find_elements_by_id('password')[0].send_keys('Himagga11!')
time.sleep(4)
# print('password successful')
driver.find_element_by_class_name('login__form_action_container').click()
time.sleep(2)
driver.find_element_by_class_name('btn__primary--large').click()
# print("entered Home page")
driver.find_element_by_id('ember24').click()
time.sleep(2)
driver.find_element_by_class_name('jobs-search-box__inner').click()
time.sleep(2)
driver.switch_to.active_element.send_keys('data analyst')
time.sleep(2)
driver.switch_to.active_element.send_keys(Keys.TAB)
time.sleep(2)
driver.switch_to.active_element.send_keys('Madrid')
time.sleep(3)
driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
time.sleep(2)
driver.switch_to.active_element.send_keys(Keys.ENTER)
time.sleep(3)
# CLICK ON THE Experience Level drop down
driver.find_elements_by_class_name('search-reusables__pill-button-caret-icon')[1].click()
# this index 1 is for the second element on the page that has a down arrow (in the
# group of date posted, experience level, company, job type)
time.sleep(2)
# Selecting Entry Level Jobs
driver.find_elements_by_class_name('search-reusables__value-label')[5].click()
time.sleep(2)
driver.find_elements_by_class_name('search-reusables__pill-button-caret-icon')[1].click()
time.sleep(2)
driver.find_element_by_css_selector('.msg-overlay-bubble-header__details').click()
time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
time.sleep(3)

job_cards = soup.find_all('li', {'class': re.compile('jobs-search-results*')})
# Now for each job card , we will start scraping the data
jobs_card_data = {}
for job_card in job_cards:

        # time the job was posted
        try:
                job_card_time_text = job_card.find('time').text
                posted_time = re.findall('\w+', job_card_time_text)
                time_posted = " ".join(posted_time)
        except AttributeError:
                time_posted = ''

        # Actively Recruiting
        try:
                actively_recruiting = job_card.find('span', {'class': re.compile('job-flavors*')}).text
                actively_recruiting = re.findall('\w+', actively_recruiting)
                actively_recruiting = " ".join(actively_recruiting)
        except AttributeError:
                actively_recruiting = ''


        # location
        try:
                location = job_card.find('li', {'class':re.compile('job-card-container*')}).text
                location = re.findall('\w+', location)
                location = " ".join(location)
        except AttributeError:
                location = ''

        # company
        try:
                company_name = job_card.find('a', {'class': re.compile('job-card-container__link job-card-container__company-name*')}).text
                company_name = re.findall('\w+', company_name)
                company_name = " ".join(company_name)
        except AttributeError:
                company_name = ''

        # position
        try:
                position = job_card.find('a', {'class': re.compile("disabled ember-view job-card-container__link job-card-list__title*")}).text
                position = re.findall('\w+', position)
                position = " ".join(position)
        except AttributeError:
                position = ''

        if company_name != '':
                jobs_card_data[company_name] = [position, location, time_posted, actively_recruiting]







time.sleep(3)