

import pandas as pd
from bs4 import BeautifulSoup 
import requests
from splinter import Browser



master_dict = {}

def scrape():
    print("fetching data")
    
  
    scrape_article()
    featured_image()
    mars_tweets()    
    get_facts()
    get_urls()
    print("Done!")
    return master_dict


master_dict = {}



def scrape_article(): 
    mars_news = []
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('div', attrs={'class': 'content_title'}).get_text()
    title = title.replace('\n', '')
    article = soup.find('div', attrs={'class': 'rollover_description_inner'}).get_text()
    article = article.replace('\n', '')
    mars_news.append( {
        'title' : title,
        'article' : article
    })
    master_dict['news'] = mars_news





def featured_image():
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path':'/Users/ehamilton/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path)
    browser.visit(featured_image_url)
    content= browser.html
    JPL_soup = BeautifulSoup(content, 'html.parser')
    url = JPL_soup.article['style']
    clean = url.split("'")[1]
    clean.replace("'", "")
    featured_image_url = 'https://www.jpl.nasa.gov' + clean
    browser.quit()
    master_dict['featured_image'] = featured_image_url



def mars_tweets():
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    tweet_response = requests.get(mars_twitter)
    twitter_soup = BeautifulSoup(tweet_response.content, 'html.parser')
    mars_weather = twitter_soup.find('p', 'tweet-text').get_text()
    master_dict['mars_tweets'] = mars_weather



def get_facts():
    mars_facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_facts_url)
    facts_table = facts_table[0]
    facts_table.rename(columns= {0 : 'Mars', 1 : 'Facts'}, inplace=True)
    facts_table['Facts'] = map(lambda x: x.encode('ascii', 'ignore').decode('ascii'), facts_table["Facts"])
    table = facts_table.to_html()
    master_dict['facts'] = table



def get_urls():
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_response = requests.get(hemi_url)
    hemi_soup = BeautifulSoup(hemi_response.content, 'html.parser')
    img_urls = hemi_soup.find_all("a", {"class": "itemLink product-item"})
    img_urls = [str(x) for x in img_urls]
    img_urls = [x.split('"')[3] for x in img_urls]
    img_urls = ["https://astrogeology.usgs.gov"+x for x in img_urls]
    title = hemi_soup.find_all('h3')
    title = [str(x) for x in title]
    title = [x.replace('<h3>',' ').replace('</h3>',' ') for x in title]
    hemisphere_image_urls = []
    for t, i in zip(title, img_urls):
        hemisphere_image_urls.append( {
            "title" : t,
            'img_url' : i
        })
        print(t, i)
        
    hemisphere_image_urls
    master_dict['hemi_img_urls'] = hemisphere_image_urls
    







