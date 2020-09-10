import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import re

def scrape():
    # initialize chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #  Create dictionary to store scraped data
    mars_dictionary = {}
    # Task 1:  Nasa Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    # use splinter browser to visit page and check for element with mars news title and subtitle
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    # Select first news item in list
    news_element = soup.select_one("ul.item_list li.slide")
    result_title = news_element.find('div', class_="content_title")
    news_title = result_title.text
    result_paragraph = news_element.find('div', class_="rollover_description_inner")
    paragraph_text = result_paragraph.text
    # add title and paragraph to dictionary
    mars_dictionary['news_title'] = news_title
    mars_dictionary['news_paragraph'] = paragraph_text

    # Task 2:  JPL Mars Space Images - Featured Image
    # JPL Mars Space Images - Featured Image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)
    #first_button = browser.links.find_by_name('data-fancybox-href').first
    first_button = browser.links.find_by_partial_text('FULL IMAGE')
    html = browser.html
    soup = bs(html, 'html.parser')
    footer = soup.footer.find('a')
    featured_image_url = base_url + footer['data-fancybox-href']
    # add featured image url to dictionary
    mars_dictionary['featured_image_url'] = featured_image_url


    # Task 3:   Mars weather (twitter)
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    result_tweet = soup.find('div', class_="js-tweet-text-container")
    #result_tweet = soup.find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    mars_weather = result_tweet.text
    # Remove first word and last item in tweet
    start_pos = mars_weather.find(' ') + 1
    end_pos = mars_weather.rfind(' ')
    mars_weather = mars_weather[start_pos:end_pos]
    print(mars_weather)
    # add mars weather to dictionary
    mars_dictionary['mars_weather'] = mars_weather

    # Task 4:   Mars Facts
    # Mars facts
    # URL of page to be scraped
    url = "https://space-facts.com/mars/"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    # results are returned as an iterable list
    mars_facts_table = soup.find('table', class_="tablepress tablepress-id-p-mars", id="tablepress-p-mars" )
    mars_facts_rows = mars_facts_table.find_all('tr')
    mars_facts = []
    for row in mars_facts_rows:
        row_description = row.find('td', class_='column-1').text
        row_value = row.find('td', class_='column-2').text
        fact_dict = {'description': row_description, 'value': row_value}
        mars_facts.append(fact_dict)

    # add mars facts table to dictionary
    mars_dictionary['mars_facts'] = mars_facts
    #mars_dictionary['mars_facts_table'] = "'" + str(mars_facts_table) + "'"

    # Task 5:   Mars hemispere photos
    # URL of page to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    mars_hemispheres_results = soup.find_all('a', class_="itemLink product-item")
    # iterate through mars_hemispheres_results and go to each href to get the full url for the high res. hemisphere image
    hemisphere_image_urls = []
    for item in mars_hemispheres_results:
        url_to_visit = base_url + item['href']
        browser.visit(url_to_visit)
        print(url_to_visit)
        # Retrieve page with the requests module
        response = requests.get(url_to_visit)
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(response.text, 'html.parser')
        #result_title = soup.find('div', class_="content")
        result_title = soup.find('h2', class_="title")
        result_title = result_title.text
        new_title = result_title[:-9]
        print(new_title)

        result_download = soup.find('div', class_='downloads')
        result_url = result_download.a['href']
        print(result_url)
        print()
        result_dict = {'hemisphere_name': new_title, 'hemisphere_url':result_url}
        hemisphere_image_urls.append(dict(result_dict))

    # add dictionary of hemisphere photo urls to dictionary
    mars_dictionary['hemisphere_image_urls'] = hemisphere_image_urls
    print(mars_dictionary)
    print('done with scraping')
    return mars_dictionary


def insert_mars_data(mars_dict):
    from pymongo import MongoClient

    # Setup a connection to `store_inventory` and the `produce` collection using `pymongo`.
    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    client = MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    # db = client.db = client.mission_to_mars
    db = client.mission_to_mars
    # Drop collection if available
    db.mars_info.drop()

    # Creates a collection in the database and inserts two documents
    db.mars_info.insert_one(mars_dict)
