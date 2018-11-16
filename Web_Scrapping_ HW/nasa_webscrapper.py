#Import Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# save the most recent article, title and date
#Get Headlines():
def getHeadLines():
    browser = init_browser()
    # Visit the NASA news URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    news_dict = {}
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text
    # print(news_date)
    # print(news_title)
    # print(news_p)

    news_dict["title"] = news_title
    news_dict["news"] = news_p
    news_dict["Date"] = news_date 

    browser.quit()
    return news_dict

# news = getHeadLines()
# print(news)

#featured image 
def getFtImage():
    browser = init_browser()
    urla= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(urla)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_dict = {}
    ft_images = soup.find('section', class_='centered_text clearfix main_feature primary_media_feature single')
    #ft_images
    link = ft_images.find('article')
    url = link['style']

    featured_image_url= { "image": ('https://www.jpl.nasa.gov/' + url[23:75])}
    #print(featured_image_url)

    image_dict["image"] = featured_image_url

    browser.quit()
    return image_dict

# ftimage = getFtImage()
# print(ftimage)

#twitter scrape
def twitterScrape():
    browser = init_browser()
    urlb = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(urlb)

    html = browser.html
    soup = bs(html,'html.parser')  

    twitter_dict ={}
  
    tweets = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather_tweets = tweets.text
    mars_weather = {"surface_weather" : weather_tweets}
    #print(mars_weather)

    twitter_dict["surface_weather"] = weather_tweets

    browser.quit()
    return twitter_dict

# tweet = twitterScrape()
# print(tweet)

def marsTable():

    urlc = 'http://space-facts.com/mars/'

    tables = pd.read_html(urlc)

    df = tables[0]
    df.columns=["Description","Value"]
    df.set_index('Description')
    table = df.to_html(classes=["table table-striped"])
    mars_table = {"table" : table}

    return mars_table

# table = marsTable()
# print(table)

def getResults():
    browser = init_browser()
    urld = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(urld)

    html = browser.html
    soup = bs(html, 'html.parser')
    
    results_dict={}

    results = soup.find_all(class_='item')
    hemisphere_image_url = []
    mars_hemisphere ={}
    for result in results:
        img = result.find('img')
        img_url = img['src']
        title = result.find('h3').text
        mars_hemisphere.update({title:('https://astrogeology.usgs.gov'+img_url)})
        mars_hemisphere ={"title" : title, "image_url" : ("https://astrogeology.usgs.gov" + img_url)}
        print(mars_hemisphere)
        hemisphere_image_url.append(mars_hemisphere)
        print(hemisphere_image_url)

    results_dict["hemi"] = hemisphere_image_url
    print(results_dict)

    browser.quit()
    return results_dict

# hemi = getResults()
# print(hemi)


def getMarsFacts():

    headlines = getHeadLines()

    image = getFtImage()
    twit = twitterScrape()
    tbl = marsTable()
    res = getResults()

    mars_dict = {}

    mars_dict["News"] = headlines
    mars_dict["FeaturedImage"] = image
    mars_dict["WeatherTweets"] = twit
    mars_dict["Table"] = tbl
    mars_dict["Hemisphere"] = res
    
    return mars_dict

#final_facts = getMarsFacts()
#print(final_facts)



   
    
