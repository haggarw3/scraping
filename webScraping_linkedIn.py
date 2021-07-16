from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import requests
import re
from bs4 import BeautifulSoup
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
time.sleep(4)


def scrape_more_info(emberID):
        content = driver.page_source
        content_soup = BeautifulSoup(content, 'lxml')
        right_rail_soup = content_soup.find('section', {'class': 'jobs-search__right-rail'})

        views = right_rail_soup.findAll('span', {'class': re.compile('jobs-details*')})[1].text
        views = re.findall('\w+', views)
        views = " ".join(views)

        job_details = right_rail_soup.find_all('span', {'class': 'jobs-details-job-summary__text--ellipsis'})
        applicants = job_details[0].text
        applicants = re.findall('\w+', applicants)
        applicants = " ".join(applicants)

        job_type = job_details[1].text
        job_type = re.findall('\w+', job_type)
        job_type = " ".join(job_type)

        # Company Details:
        employees = job_details[2].text
        employees = re.findall('\S+', employees)
        employees = " ".join(employees)

        sector = job_details[2].text
        sector = re.findall('\S+', sector)
        sector = " ".join(sector)

        descriptions = right_rail_soup.find('div', {'id': 'job-details'}).find('span').text
        descriptions = re.findall('\w+', descriptions)
        descriptions = " ".join(descriptions)

        other_details = right_rail_soup.find('div', {'class': 'jobs-description-details pt4'})
        industry = other_details.find_all('li', {'class': 'jobs-description-details__list-item t-14'})[0].text
        industry = re.findall('\w+', industry)
        industry = " ".join(industry)

        job_functions = other_details.find_all('li', {'class': 'jobs-description-details__list-item t-14'})[1].text
        job_functions = re.findall('\w+', job_functions)
        job_functions = " ".join(job_functions)

        # About the company

        try:
                css_sel = "#"+emberID
                driver.find_element_by_css_selector(css_sel).send_keys(Keys.END)
                driver.find_element_by_class_name('inline-show-more-text__link-container-collapsed').click()
                about = driver.page_source
                about_company_soup = BeautifulSoup(about, 'lxml')
                company_info = about_company_soup.find('div', {'class': 'inline-show-more-text'}).text
                company_info = re.findall('\w+', company_info)
                company_info = " ".join(company_info)
        except AttributeError:
                company_info = about_company_soup.find('div', {'class': 'inline-show-more-text'}).text
                company_info = re.findall('\w+', company_info)
                company_info = " ".join(company_info)

        time.sleep(5)
        return [views, applicants, job_type, employees, sector, descriptions, industry, job_functions, company_info]


jobs_card_data = {}
df = pd.DataFrame(['company_name', 'position', 'location', 'time_posted', 'date_posted', 'actively_recruiting', 'Number of applications', 'Other_info'])
counter = 1
page = 1

# To find the max number of pages after the filter

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
time.sleep(3)
max_pages = soup.find_all('button', {'aria-label': re.compile('Page*')})[-1].text
max_pages = re.findall('\d+', max_pages)[0]
max_pages = int(max_pages)


while page < max_pages:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(3)
        job_cards = soup.find_all('li', {'class': re.compile('jobs-search-results*')})

        # Now for each job card , we will start scraping the data
        
        for job_card in job_cards:

                # time the job was posted
                try:
                        job_card_time_text = job_card.find('time').text
                        posted_time = re.findall('\w+', job_card_time_text)
                        time_posted = " ".join(posted_time)
                        date_posted = job_card.find('time').attrs['datetime']
                except AttributeError:
                        time_posted = ''
                        date_posted = ''

                # Actively Recruiting
                try:
                        actively_recruiting = job_card.find('span', {'class': re.compile('job-flavors*')}).text
                        actively_recruiting = re.findall('\w+', actively_recruiting)
                        actively_recruiting = " ".join(actively_recruiting)
                except AttributeError:
                        actively_recruiting = ''

                # location
                try:
                        location = job_card.find('li', {'class': re.compile('job-card-container__metadata-item*')}).text
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
                        try:
                                company_name = job_card.find('div', {'class': re.compile('job-card-container__company-name*')}).text
                                company_name = re.findall('\w+', company_name)
                                company_name = " ".join(company_name)
                        except AttributeError:
                                company_name = ''

                # position
                try:
                        position = job_card.find('a', {'class': re.compile("disabled ember-view job-card-container__link job-card-list__title*")}).text
                        position = re.findall('\w+', position)
                        position = " ".join(position)

                        # Finding the ember ID to be able to click on it

                        emberID = job_card.find('a', {
                                'class': re.compile("disabled ember-view job-card-container__link job-card-list__title*")})
                        emberID = emberID.attrs['id']
                        driver.find_element_by_id(emberID).click()
                        time.sleep(2)
                        # Function call to get more info
                        more_results = scrape_more_info(emberID)

                except AttributeError:
                        position = ''

                # applications

                try:
                        applications = job_card.find('a', {'class': re.compile("job-card-container__applicant-count job-card-container__footer-item job-card-container*")}).text
                        applications = re.findall('\w+', applications)
                        applications = " ".join(applications)
                except AttributeError:
                        applications = ''

                if company_name != '':
                        jobs_card_data[counter] = [company_name, position, location, time_posted, date_posted, actively_recruiting, applications, more_results]

                counter += 1


        

        page += 1




# temp = pd.DataFrame(jobs_card_data).T
# df = pd.concat([df, temp])
# df = df.reset_index()




time.sleep(3)
