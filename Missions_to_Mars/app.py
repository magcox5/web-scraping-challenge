import numpy as np
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
# setup mongo connection
#conn = 'mongodb://localhost:27017'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# connect to mongo db and collection
#client = PyMongo.MongoClient(conn)
#db = client.mission_to_mars

#################################################
# Flask Routes
#################################################

@app.route("/")
def go_mongo():
    """Query Mongo db and pass mars data into HTML template"""
    mission = mongo.db.mars_info.find_one()
    return render_template('index.html', mission=mission)

@app.route("/scrape")
def go_scrape_mars():
    # get new mars data, pass to .html file, and save in mongo db
    mars_info = mongo.db.mars_info
    mars_dict = scrape_mars.scrape()
    mars_info.update({}, mars_dict, upsert=True)
    #return render_template('index.html', mission=mission)
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
