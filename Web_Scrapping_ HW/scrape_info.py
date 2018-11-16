from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from flask import Flask, render_template, redirect

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def Scrape_One():
   browser = init_browser()


   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)
   html = browser.html
   soup = bs(html, 'html.parser')

   articles = soup.find('li', class_='slide')

   text = articles.find(class_='list_text')
   news_title = text.find(class_='content_title')
   news_title_name = news_title.find('a').get_text()
   news_p = text.find(class_='article_teaser_body').get_text()

   marsnews = {"title" : news_title_name,"news" : news_p}

   return marsnews


def Scrape_Two():
   browser = init_browser()


   url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url)
   html = browser.html
   soup = bs(html,'html.parser')

   images = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
   link = images.find('article')
   url = link['style']

   marspic= { "image": ('https://www.jpl.nasa.gov/' + url[23:75])}

   return marspic

def Scrape_Three():
   browser = init_browser()


   url = 'https://twitter.com/marswxreport?lang=en'
   browser.visit(url)
   html = browser.html
   soup = bs(html,'html.parser')

   tweets = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
   tweetweather = tweets.text

   marsweather = {"surface weather" : tweetweather}
   return marsweather


def Scrape_Four():
   url = 'http://space-facts.com/mars/'
   #select columns and 0 table
   #used df and then column headings
   tables = pd.read_html(url)
   df = tables[0]
   df.columns=["Description","Value"]
   df.set_index('Description')
   mars_table = df.to_html(classes=["table table-striped"])

   marstable = {"table" : mars_table}

   return marstable

def Scrape_Five():
   browser = init_browser()

   url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(url)
   html = browser.html
   soup = bs(html, 'html.parser')

   results = soup.find_all(class_='item')

   marshemi ={}
   for result in results:
       img = result.find('img')
       img_url = img['src']
       title = result.find('h3').text
       marshemi.update({title:('https://astrogeology.usgs.gov'+img_url)})

   marshemi ={"title" : title, "image_url" : ("https://astrogeology.usgs.gov" + img_url)}

   return marshemi