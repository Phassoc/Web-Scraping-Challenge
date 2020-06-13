{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: splinter in c:\\users\\phass\\anaconda3\\lib\\site-packages (0.13.0)\n",
      "Requirement already satisfied: six in c:\\users\\phass\\anaconda3\\lib\\site-packages (from splinter) (1.12.0)\n",
      "Requirement already satisfied: selenium>=3.141.0 in c:\\users\\phass\\anaconda3\\lib\\site-packages (from splinter) (3.141.0)\n",
      "Requirement already satisfied: urllib3 in c:\\users\\phass\\anaconda3\\lib\\site-packages (from selenium>=3.141.0->splinter) (1.24.2)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install splinter"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup as bs\n",
    "import requests\n",
    "from splinter import Browser\n",
    "import os\n",
    "import pandas as pd\n",
    "import time"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Create function for accessing Windows Chrome Driver"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Windows chromedriver.exe function to choose the executable path to driver\n",
    "def get_browser():\n",
    "    executable_path = {\"executable_path\": \"C:/users/phass/chromedriver\"}\n",
    "    return Browser(\"chrome\", **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## NASA Mars News"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Run init_browser/driver.\n",
    "browser = get_browser()\n",
    "\n",
    "# Visit Nasa news url.\n",
    "news_url = \"https://mars.nasa.gov/news/\"\n",
    "browser.visit(news_url)\n",
    "\n",
    "time.sleep(5)\n",
    "\n",
    "# HTML Object.\n",
    "html = browser.html\n",
    "\n",
    "# Parse HTML with Beautiful Soup\n",
    "news_soup = bs(html, \"html.parser\")\n",
    "\n",
    "# Retrieve the most recent article's title and paragraph.\n",
    "# Store in news variables.\n",
    "news_title = news_soup.find(\"div\", class_=\"content_title\").text\n",
    "news_paragraph = news_soup.find(\"div\", class_=\"article_teaser_body\").text\n",
    "\n",
    "# Exit Browser.\n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mars Now\n",
      "-----------------------------------------\n",
      "Two astronauts collected Moon rocks on Apollo 11. It will take three robotic systems working together to gather up the first Mars rock samples for return to Earth.\n"
     ]
    }
   ],
   "source": [
    "# Display scraped news \n",
    "print(news_title)\n",
    "print(\"-----------------------------------------\")\n",
    "print(news_paragraph)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## JPL Mars Space Images - Featured Image"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Run init_browser/driver.\n",
    "browser = get_browser()\n",
    "\n",
    "# Visit the url for JPL Featured Space Image.\n",
    "jpl_url = \"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars\"\n",
    "browser.visit(jpl_url)\n",
    "\n",
    "# Select \"FULL IMAGE\".\n",
    "browser.click_link_by_partial_text(\"FULL IMAGE\")\n",
    "\n",
    "# Find \"more info\" for first image, set to variable, and command click.\n",
    "browser.is_element_present_by_text(\"more info\", wait_time=1)\n",
    "more_info_element = browser.find_link_by_partial_text(\"more info\")\n",
    "more_info_element.click()\n",
    "\n",
    "time.sleep(5)\n",
    "\n",
    "# HTML Object.\n",
    "html = browser.html\n",
    "\n",
    "# Parse HTML with Beautiful Soup\n",
    "image_soup = bs(html, \"html.parser\")\n",
    "\n",
    "# Scrape image URL.\n",
    "image_url = image_soup.find(\"figure\", class_=\"lede\").a[\"href\"]\n",
    "\n",
    "# Concatentate https://www.jpl.nasa.gov with image_url.\n",
    "featured_image_url = f'https://www.jpl.nasa.gov{image_url}'\n",
    "\n",
    "# Exit Browser.\n",
    "browser.quit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA02570_hires.jpg\n"
     ]
    }
   ],
   "source": [
    "print(featured_image_url)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'InSight sol 543 (2020-06-06) low -92.9ºC (-135.3ºF) high -6.6ºC (20.2ºF) winds from the WNW at 7.2 m/s (16.0 mph) gusting to 21.0 m/s (47.0 mph) pressure at 7.40 hPa'"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Run init_browser/driver.\n",
    "browser = get_browser()\n",
    "\n",
    "# Visit the url for Mars Weather twitter account.\n",
    "weather_url = \"https://twitter.com/marswxreport?lang=en\"\n",
    "browser.visit(weather_url)\n",
    "\n",
    "time.sleep(5)\n",
    "\n",
    "# HTML Object.\n",
    "html = browser.html\n",
    "\n",
    "# Parse HTML with Beautiful Soup\n",
    "weather_soup = bs(html, \"html.parser\")\n",
    "\n",
    "mars_weather = weather_soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')\\\n",
    ".find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text\n",
    "\n",
    "mars_weather = mars_weather.replace('\\n', ' ')\n",
    "\n",
    "mars_weather\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Value</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Description</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <td>Equatorial Diameter:</td>\n",
       "      <td>6,792 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Polar Diameter:</td>\n",
       "      <td>6,752 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Mass:</td>\n",
       "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Moons:</td>\n",
       "      <td>2 (Phobos &amp; Deimos)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Orbit Distance:</td>\n",
       "      <td>227,943,824 km (1.38 AU)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Orbit Period:</td>\n",
       "      <td>687 days (1.9 years)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Surface Temperature:</td>\n",
       "      <td>-87 to -5 °C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>First Record:</td>\n",
       "      <td>2nd millennium BC</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <td>Recorded By:</td>\n",
       "      <td>Egyptian astronomers</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              Value\n",
       "Description                                        \n",
       "Equatorial Diameter:                       6,792 km\n",
       "Polar Diameter:                            6,752 km\n",
       "Mass:                 6.39 × 10^23 kg (0.11 Earths)\n",
       "Moons:                          2 (Phobos & Deimos)\n",
       "Orbit Distance:            227,943,824 km (1.38 AU)\n",
       "Orbit Period:                  687 days (1.9 years)\n",
       "Surface Temperature:                   -87 to -5 °C\n",
       "First Record:                     2nd millennium BC\n",
       "Recorded By:                   Egyptian astronomers"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Visit the Mars Facts webpage and use Pandas to scrape the table\n",
    "url_facts = \"https://space-facts.com/mars/\"\n",
    "\n",
    "# Use Pandas - read_html - to scrape tabular data from a page\n",
    "mars_facts = pd.read_html(url_facts)\n",
    "#mars_facts\n",
    "\n",
    "mars_df = mars_facts[0]\n",
    "\n",
    "# Create Data Frame\n",
    "mars_df.columns = [\"Description\", \"Value\"]\n",
    "\n",
    "# Set index to Description\n",
    "mars_df.set_index(\"Description\", inplace=True)\n",
    "\n",
    "# Save html code to folder Assets\n",
    "html_table = mars_df.to_html()\n",
    "\n",
    "# Strip unwanted newlines to clean up the table\n",
    "html_table.replace(\"\\n\", '')\n",
    "\n",
    "# Save html code\n",
    "mars_df.to_html(\"mars_facts_data.html\")\n",
    "\n",
    "# Print Data Frame\n",
    "mars_df\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Mars Hemispheres"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "browser = get_browser()\n",
    "\n",
    "url_hemisphere = \"https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars\"\n",
    "browser.visit(url_hemisphere)\n",
    "\n",
    "time.sleep(5)\n",
    "\n",
    "# HTML Object\n",
    "html_hemisphere = browser.html\n",
    "soup = bs(html_hemisphere, \"html.parser\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Cerberus Hemisphere Enhanced\n",
      "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg\n",
      "-----------------------------------------\n",
      "\n",
      "Schiaparelli Hemisphere Enhanced\n",
      "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg\n",
      "-----------------------------------------\n",
      "\n",
      "Syrtis Major Hemisphere Enhanced\n",
      "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg\n",
      "-----------------------------------------\n",
      "\n",
      "Valles Marineris Hemisphere Enhanced\n",
      "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg\n",
      "-----------------------------------------\n"
     ]
    }
   ],
   "source": [
    "# Scrape all items that contain mars hemispheres information\n",
    "hemispheres = soup.find_all(\"div\", class_=\"item\")\n",
    "\n",
    "# Create empty list\n",
    "hemispheres_info = []\n",
    "\n",
    "# Sign main url for loop\n",
    "hemispheres_url = \"https://astrogeology.usgs.gov\"\n",
    "\n",
    "# Loop through the list of all hemispheres information\n",
    "for i in hemispheres:\n",
    "    title = i.find(\"h3\").text\n",
    "    hemispheres_img = i.find(\"a\", class_=\"itemLink product-item\")[\"href\"]\n",
    "    \n",
    "    # Visit the link that contains the full image website \n",
    "    browser.visit(hemispheres_url + hemispheres_img)\n",
    "    \n",
    "    # HTML Object\n",
    "    image_html = browser.html\n",
    "    web_info = bs(image_html, \"html.parser\")\n",
    "    \n",
    "    # Create full image url\n",
    "    img_url = hemispheres_url + web_info.find(\"img\", class_=\"wide-image\")[\"src\"]\n",
    "    \n",
    "    hemispheres_info.append({\"title\" : title, \"img_url\" : img_url})\n",
    "\n",
    "# Display titles and images ulr\n",
    "#hemispheres_info\n",
    "\n",
    "# Or Display titles and images ulr this way\n",
    "    print(\"\")\n",
    "    print(title)\n",
    "    print(img_url)\n",
    "    print(\"-----------------------------------------\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernel_info": {
   "name": "python3"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  },
  "latex_envs": {
   "LaTeX_envs_menu_present": true,
   "autoclose": false,
   "autocomplete": true,
   "bibliofile": "biblio.bib",
   "cite_by": "apalike",
   "current_citInitial": 1,
   "eqLabelWithNumbers": true,
   "eqNumInitial": 1,
   "hotkeys": {
    "equation": "Ctrl-E",
    "itemize": "Ctrl-I"
   },
   "labels_anchors": false,
   "latex_user_defs": false,
   "report_style_numbering": false,
   "user_envs_cfg": false
  },
  "nteract": {
   "version": "0.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
