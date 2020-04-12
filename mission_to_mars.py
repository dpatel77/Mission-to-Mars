#!/usr/bin/env python
# coding: utf-8

# ### NASA Mars News
# 
# * Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
# 
# ```python
# # Example:
# news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
# 
# news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
# ```

# In[2]:


get_ipython().system('pip install splinter')


# In[2]:


# Dependencies
import os
from bs4 import BeautifulSoup
import requests
import pprint
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html

# # Read HTML from file
# filepath = os.path.join("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
# with open(filepath) as file:
#     html = file.read()
    

url = 'https://mars.nasa.gov/news/'
response  = requests.get(url)
response
# /html/body/div[3]/div/div[3]/div[3]/div/article/div/section/div/ul/li[1]/div/div/div[2]/a


# In[3]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')

# tbs =soup.title.text.strip()
# results = soup.find_all('div',class_="content_title")##class_="rollover_description_inner")
results = soup.find_all('div',class_='slide')


# In[4]:


# Loop through returned results
headlines=[]
headlines

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


# In[5]:


headlines[0]


# ### JPL Mars Space Images - Featured Image
# 
# * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called `featured_image_url`.
# 
# * Make sure to find the image url to the full size `.jpg` image.
# 
# * Make sure to save a complete url string for this image.
# 
# ```python
# # Example:
# featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
# ```

# In[6]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

slides = soup.find('div', class_="carousel_items")
a = slides.find('a')
href = a['data-fancybox-href']
featured_image_url = 'https://www.jpl.nasa.gov' + href
featured_image_url


# ### Mars Weather
# 
# * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
# 
# ```python
# # Example:
# mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
# ```

# In[7]:


twitter_url = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(twitter_url)
soup = BeautifulSoup(response.text, 'html.parser')

result = soup.find('div', class_="js-tweet-text-container")
tweet = result.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
mars_weather = tweet
mars_weather


# ### Mars Facts
# 
# * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# 
# * Use Pandas to convert the data to a HTML table string.

# In[8]:


mars_html = pd.read_html("https://space-facts.com/mars/")[2].to_html()
mars_html


# ### Mars Hemispheres
# 
# * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
# 
# * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# 
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
# 
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
# 
# ```python
# # Example:
# hemisphere_image_urls = [
#     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#     {"title": "Cerberus Hemisphere", "img_url": "..."},
#     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
# ]
# ```

# In[12]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)

url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url_hemi)

# HTML object
html_hemi = browser.html

# Parse HTML with Beautiful Soup
soup_hemi = BeautifulSoup(html_hemi, 'html.parser')

# Retrieve all elements that contain book information
items = soup_hemi.find_all('div', class_='item')

hemisphere_image_urls = []

# Iterate through each book
for item in items:
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    link = item.find('a')
    href = link['href']
    titles = item.find('h3').text
    print(titles)
    urls = 'https://astrogeology.usgs.gov' + href
    print(urls)

    try:
        browser.visit(urls)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        soups = soup.find_all('div',class_="content")

        for soup in soups:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            link = soup.find('a')['href']
            print(link)
            hemisphere_image_urls.append({"title": titles, "img_url": urls,"imglink": link})
    except:
        print("Scraping skipped")


# In[13]:


hemisphere_image_urls


# - - -
# 
# ## Step 2 - MongoDB and Flask Application
# 
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
# 
# * Start by converting your Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
# 
# * Next, create a route called `/scrape` that will import your `scrape_mars.py` script and call your `scrape` function.
# 
#   * Store the return value in Mongo as a Python dictionary.
# 
# * Create a root route `/` that will query your Mongo database and pass the mars data into an HTML template to display the data.
# 
# * Create a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.
# 
# ![final_app_part1.png](Images/final_app_part1.png)
# ![final_app_part2.png](Images/final_app_part2.png)
# 
# - - -

# In[ ]:





# ## Step 3 - Submission
# 
# To submit your work to BootCampSpot, create a new GitHub repository and upload the following:
# 
# 1. The Jupyter Notebook containing the scraping code used.
# 
# 2. Screenshots of your final application.
# 
# 3. Submit the link to your new repository to BootCampSpot.
# 
# ## Hints
# 
# * Use Splinter to navigate the sites when needed and BeautifulSoup to help find and parse out the necessary data.
# 
# * Use Pymongo for CRUD applications for your database. For this homework, you can simply overwrite the existing document each time the `/scrape` url is visited and new data is obtained.
# 
# * Use Bootstrap to structure your HTML template.
# 
# ### Copyright
# 
# Trilogy Education Services © 2019. All Rights Reserved.

# In[ ]:




