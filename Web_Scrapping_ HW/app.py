from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from flask import Flask, render_template, redirect
import scrape_info 

app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db
Mars = db.items

if __name__ == '__main__':
    app.run()

@app.route("/")
def echo():
    Mars = db.items
    #Mars = mongo.db.Mars.find()
    return render_template("index.html", mars = Mars)

@app.route("/scrape")
def scrape():
   Mars = db.items #mongo.db.Mars

#tried a different way by making a dictionary in each scrape, then a new dict here

   mars_news = scrape_info.scrape_one()
   mars_picture = scrape_info.scrape_two()
   mars_weathers = scrape_info.scrape_three()
   mars_table = scrape_info.scrape_four()
   mars_hemi = scrape_info.scrape_five()

   Mars_Dict = {
       "Headline": mars_news["title"],
       "News": mars_news["news"],
       "Image": mars_picture["image"],
       "Weather": mars_weather["surface weather"],
       "Table": mars_table["table"],
       "Hemisphere": mars_hemi["title"],
       "Hemitwo": mars_hemi["image_url"]
   }

   Mars.update({}, Mars_Dict, upsert=True)

