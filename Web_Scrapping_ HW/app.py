from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from flask import Flask, render_template, redirect
import nasawebscrapper

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

#give them variables

   mars_news = nasawebscrapper.getHeadLines()
   mars_picture = nasawebscrapper.getFtImage()
   mars_weathers = nasawebscrapper.twitterScrape()
   mars_table = nasawebscrapper.marsTable()
   mars_hemi = nasawebscrapper.getResults()

   Mars_Dict = {
       "Headline": mars_news["title"],
       "News": mars_news["news"],
       "Image": mars_picture["image"],
       "Weather": mars_weathers["surface_weather"],
       "Table": mars_table["table"],
       "Hemisphere": mars_hemi["hemi"],
       "Hemitwo": mars_hemi["hemi"]
   }

   Mars.update({}, Mars_Dict, upsert=True)

