import pandas as pd 
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import re
import pymongo 

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')
    result = soup.find(class_="slide")

    print(soup.prettify())

    news_title = soup.find("div", class_="content_title").get_text()
    print(news_title)

    news_par = soup.find("div", class_="rollover_description").get_text()
    print(news_par)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image = soup.find(class_='carousel_items').find('article')['style']
    link = re.search("'(.*)'", featured_image)
    image_url = "https://jpl.nasa.gov" + link.group(1)
    print(image_url)

    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)

    df = table[0]
    df = df.rename(columns={0:"Description", 1: "Value"})

    html_table = df.to_html()

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    links = browser.find_by_css("a.product-item h3")

    for l in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[l].click()
        sample_link = browser.links.find_by_text('Sample').first
        hemisphere['url'] = sample_link['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()


return mars_data





