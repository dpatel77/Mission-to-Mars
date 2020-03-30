from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pprint

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response  = requests.get(url)
    response

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # tbs =soup.title.text.strip()
    # results = soup.find_all('div',class_="content_title")##class_="rollover_description_inner")
    results = soup.find_all('div',class_='slide')

    # Loop through returned results
    headlines=[]

    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            title = result.find(class_="content_title").a.text
            # Identify and return price of listing
            paragraph = result.find(class_="rollover_description_inner").text
            if (title and paragraph):
                # And the anchor has non-blank text...
                # Append the td to the list
                headlines.append({'title':title,'paragraph':paragraph})
                    

            # Print results only if title, price, and link are available
            if (title and paragraph):
                print('-------------')
                print(title)
                print(paragraph)
        except AttributeError as e:
            print(e)


    # Close the browser after scraping
    browser.quit()

    # Return results
    return headlines
