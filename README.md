# **Mission to Mars**
This program scrapes Mars data from the following websites in order to create a fact sheet with Mars images as a local web page.
- Nasa Mars news
- Jet Propulsion Labs
- Twitter account with Mars weather
- Mars Facts
- USGS Astrogeology site for images of Mars' Hemispheres

#### Note:  Twitter disable access to tweet texts, so I used Tweepy and the Twitter api to get the weather. Technically not scraping.

# ***Files:***
(Written in python)
- app.py is the flask application server
- scrape_mars.py is the file converted from the jupyter notebook to scrape the data
- mission_to_mars.ipynb is the jupyter notebook
- template\index.html is the home page for the server
- chromedrive.exe -- essential for scraping the data 

# ***Database:***
- MongoDB - Database is called mission_to_mars, Collection is called mars_info. Every time new data is scraped, the old database is dropped and a new one is created.

# ***Instructions:***
1. Prerequisites:
    1.  All files listed above - download to a new subdirectory
    1.  Python
    1.  Chromedrive (goes to target website to scrape data)
    1.  Tweepy       (to get data from Twitter api)
    1.  Pandas       
    1.  Beautiful Soup (tool for parsing scraped data)
    1.  requests
    1.  splinter/browser (used with Chromedrive)
    1.  re
    1.  A config.py file with your Twitter authorization credentials
    1. PyMongo  (to interact with MongoDB)
    1. Jupyter Notebook (If you want to run pieces of code in mission_to_mars.ipynb to see how things work)
    1. Chrome browser
    1. A twitter account with access credentials for the tweets you want
    1. Flask (to create a web server to host your web page)
    

2. Run the application:
    1. Go to a terminal application, such as git bash
    1. Go to the subdirectory containing your Mars scraping files 
    1. At the command line, run the flask application 
        ***python app.py***
    1. In the chrome browser, go to ***http://127.0.0.1:5000/***
        The Mars Facts page appears. 
    1. Press ***"Scrape New Data"*** and the program will go get the latest info. from the Mars websites.

# ***Final Result:***
<img src="Mission to Mars_final-page1.jpg"> <br>

<img src="Mission to Mars_final-page2.jpg">
