# Dependencies  
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time
import re

# Browser setup function...
def get_browser():
	
		return Browser("chrome", executable_path="chromedriver", headless=True)
	
mars_info = {}
	
# Mars News
def scrape_info():
	
	browser = get_browser()
	
	# Visit Nasa news url
	news_url = "https://mars.nasa.gov/news/"
	browser.visit(news_url)

	time.sleep(5)
		
	# HTML Object
	html = browser.html
	news_soup = bs(html, "html.parser")
		
	# Scrape the latest News Title and Paragraph Text
	news_title = news_soup.find("div", class_ = "content_title").text
	news_paragraph = news_soup.find("div", class_ = "article_teaser_body").text
	
	mars_info["news_title"] = news_title
	mars_info["news_paragraph"] = news_paragraph 


# Featured Image
	
	# Visit JPL Featured Space Image url
	browser = get_browser()
	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(jpl_url)
	
    # Select "FULL IMAGE".
	browser.click_link_by_partial_text("FULL IMAGE")

    # Find "more info" for first image, set to variable, and command click.
	browser.is_element_present_by_text("more info", wait_time=1)
	more_info_element = browser.find_link_by_partial_text("more info")
	more_info_element.click()

	time.sleep(5)

	# HTML Object.
	html = browser.html

	# Parse HTML with Beautiful Soup
	image_soup = bs(html, "html.parser")

	# Scrape image URL.
	image_url = image_soup.find("figure", class_="lede").a["href"]

	# Concatentate https://www.jpl.nasa.gov with image_url.
	featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

	mars_info["featured_image_url"] = featured_image_url
	
	
# Mars Weather
	
	# Run init_browser/driver.
	browser = get_browser()

	# Visit the url for Mars Weather twitter account.
	weather_url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(weather_url)

	time.sleep(5)

	# HTML Object.
	html = browser.html

	# Parse HTML with Beautiful Soup
	weather_soup = bs(html, "html.parser")

	mars_weather = weather_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')\
	.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

	mars_weather = mars_weather.replace('\n', ' ')

	mars_info["mars_weather"] = mars_weather
	

# Mars Facts

	# Visit the Mars Facts webpage and use Pandas to scrape the table
	url_facts = "https://space-facts.com/mars/"

	# Use Pandas - read_html - to scrape tabular data from a page
	mars_facts = pd.read_html(url_facts)

	# Find the mars facts DataFrame in the list
	mars_df = mars_facts[0]

	# Create Data Frame
	mars_df.columns = ["Description", "Value"]

	# Set index to Description
	mars_df.set_index("Description", inplace=True)

	# Save html code to folder Assets
	html_table = mars_df.to_html()

	# Strip unwanted newlines to clean up the table
	html_table.replace("\n", '')

	# Save html code
	mars_df.to_html("mars_facts_data.html")

	mars_info["mars_facts"] = html_table


# Mars Hemispheres - 4
	
	# Visit the USGS Astrogeology Science Center url
	browser = get_browser()
	url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url_hemisphere)

	time.sleep(5)

	# HTML Object
	html_hemisphere = browser.html
	soup = bs(html_hemisphere, "html.parser")

	# Find containers whcih has mars hemispheres information
	hemispheres = soup.find_all("div", class_="item")

	# Create empty list
	hemispheres_info = []

	# Sign main url for loop
	hemispheres_url = "https://astrogeology.usgs.gov"

	# Loop through the list of all hemispheres information
	for i in hemispheres:
		title = i.find("h3").text
		hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
		
		# Visit the link that contains the full image website 
		browser.visit(hemispheres_url + hemispheres_img)
		
		# HTML Object
		image_html = browser.html
		web_info = bs(image_html, "html.parser")
		
		# Create full image url
		img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
		
		mars_info["title"] = title.strip()       
		mars_info["img_url"] = img_url
		
		hemispheres_info.append({"title" : title, "img_url" : img_url})

		mars_info["hemispheres_info"] = hemispheres_info

# Close the browser after scraping
	browser.quit()
	
	return mars_info



