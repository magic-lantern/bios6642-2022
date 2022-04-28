# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# some libraries that are used across examples
from pprint import pprint
import re
import time

# %% [markdown]
# # Web scraping
#
# Why web scraping?
#
# Many experts have proposed that 80% of a machine learning/AI project is spent on data gathering and preparation, with 20% spent on training a model. For more on this topic, watch Dr. Andrew Ng's presention on data centric AI availble at https://youtu.be/06-AZXmwHjo.
#
# Recently the topic of web scraping has been in the news as a high profile case has been working its way through the US legal system. Automated scraping of publicly available information is legal: https://techcrunch.com/2022/04/18/web-scraping-legal-court/ as affirmed in the various trials of LinkedIn v Hiq Labs.
#
# Data gathering is hard. If you can re-use data gathered by someone else, it can make your project possible. Note, reusing data collected for another purpose will still be hard and require quite a bit of data preparation.
#
# **The best tool to use is the one you already know.**
#
# Pandas has functionality that allows one to read in data from a variety of sources. Some include:
#
# * comma separated value or tab separated value files
# * databases (anything supported by SQLAlchemy)
# * web pages (finds all HTML tables)
#
# To learn more, see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html. Note this method doesn't support https and has a few other gotchas.
#

# %%
import pandas as pd

# %%
url = 'https://www.espn.com/mens-college-basketball/team/stats/_/id/38/colorado-buffaloes'

# %%
dfs = pd.read_html(url)
print(len(dfs))

# %% [markdown]
# You may notice when looking at the web page that it looks like two stats tables, not 4.

# %%
for df in dfs:
    print(df.head())
    print('------------')

# %% [markdown]
# It appears that the player info is in a separate table from their stats. Let's combine the two.

# %%
stats_df = pd.concat([dfs[2], dfs[3]], axis=1)
stats_df

# %% [markdown]
#
#
# ![Data Pipeline](https://imgs.xkcd.com/comics/data_pipeline.png)
#
# https://xkcd.com/2054/
#
# "Is the pipeline literally running from your laptop?"
#
# "Don't be silly, my laptop disconnects far too often to host a service we rely on. It's running on my phone."

# %%
# url = 'https://cubuffs.com/sports/mens-basketball/stats/2019-20'
url = 'https://en.wikipedia.org/wiki/Colorado_Buffaloes_men%27s_basketball'

# %%
dfs = pd.read_html(url)
print(len(dfs))

# %% [markdown]
# Compare https://en.wikipedia.org/wiki/Colorado_Buffaloes_men%27s_basketball#NCAA_Tournament_results to this

# %%
dfs[18]

# %% [markdown]
# Also note, that Pandas can create HTML - so you can use Python to create a table for a web page.

# %%
dfs[18].to_html()

# %% [markdown]
# ### Status Check
#
# https://cups.fast.ai/gitandweb

# %% [markdown]
# # More web Scraping

# %%
import re

# %%
url = 'https://www.time.gov/'

# %% [markdown]
# ## Web scraping using Requests-HTML

# %%
from requests_html import HTMLSession

# %%
session = HTMLSession()
r = session.get(url)

# %%
page_html = r.html.raw_html.decode('utf-8')

# %%
html_body = re.search(r'<body>.+</body>', page_html, flags=re.DOTALL)[0]
lines = re.findall(r'.+', html_body)
for n in range(20):
    print(lines[n])

# %%
r.html.find('time')

# %%
for t in r.html.find('time'):
    if 'id' in t.attrs.keys():
        print(f'UTC Time is: {t.text}')

# %% [markdown]
# ### What's going on?
#
# When you open the web page in your browser you can see the time. Turns out that the time portion of the website is made possible by a client side programming language called Javascript.
#
# Some history: (see https://en.wikipedia.org/wiki/JavaScript#History)
#
# > The first web browser with a graphical user interface, Mosaic, was released in 1993. Accessible to non-technical people, it played a prominent role in the rapid growth of the nascent World Wide Web. The lead developers of Mosaic then founded the Netscape corporation, which released a more polished browser, Netscape Navigator, in 1994. This quickly became the most-used.
# >
# > During these formative years of the Web, web pages could only be static, lacking the capability for dynamic behavior after the page was loaded in the browser. There was a desire in the burgeoning web development scene to remove this limitation, so in 1995, Netscape decided to add a scripting language to Navigator. They pursued two routes to achieve this: collaborating with Sun Microsystems to embed the Java programming language, while also hiring Brendan Eich to embed the Scheme language.
# > 
# > Netscape management soon decided that the best option was for Eich to devise a new language, with syntax similar to Java and less like Scheme or other extant scripting languages. Although the new language and its interpreter implementation were called LiveScript when first shipped as part of a Navigator beta in September 1995, the name was changed to JavaScript for the official release in December.
#
# Pandas and Requests-HTML, though great tools do not have a JavaScript parser built in. You need something more advanced to do that.

# %% [markdown]
# ### How to replicate this?
#
# https://www.lifewire.com/disable-javascript-in-firefox-446039
#
# https://www.lifewire.com/disable-javascript-in-google-chrome-4103631

# %% [markdown]
# ## Web scraping using Selenium and a web browser
#
# For documentation on Selenium, see:
#
# * https://selenium-python.readthedocs.io/index.html
# * https://www.selenium.dev/documentation/en/
#
# For a introductory tutorial, see https://www.scrapingbee.com/blog/selenium-python/
#
# To create Selenium scripts it can be helpful to use a test-recording tool such as [Selenium IDE](https://github.com/SeleniumHQ/selenium-ide). Selenium IDE allows you to use your browser as normal and save the actions code that can easily be edited or modified.
#
# Selenium requires additional webdriver software that allows you to control Chrome, Firefox, etc. via Python.
#
# On macOS, you can use `brew` (https://brew.sh/) to install the dependencies:
#
# ```bash
# brew install geckodriver
# brew install chromedriver
# ```
#
# On Windows 10, you can use `choco` (https://chocolatey.org/) to install the dependencies (Run this in an Administrator shell):
#
# ```powershell
# # use this line to install firefox version
# choco install selenium-gecko-driver
# # use this line to install chrome version
# choco install chromedriver
# ```

# %%
from selenium import webdriver
from IPython.display import Image
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# %%
from selenium.webdriver.firefox.options import Options as firefoxoptions
options = firefoxoptions()
# comment out this line to see what's happening
# options.headless = True
driver = webdriver.Firefox(options=options)
driver.set_window_size(1024,768)
driver.get(url)
driver.save_screenshot('firefox.png')

# %%
pprint(driver.capabilities)

# %%
Image(filename='firefox.png')

# %% [markdown]
# Alternatively use Chrome
# ```python
# from selenium.webdriver.chrome.options import Options as chromeoptions
# options = chromeoptions()
# options.headless = True
# driver = webdriver.Chrome(options=options)
# driver.set_window_size(640,480)
# driver.get(url)
# driver.save_screenshot('chrome.png')
# Image(filename='chrome.png')
# ```

# %%
page_html = driver.page_source

html_body = re.search(r'<body>.+</body>', page_html, flags=re.DOTALL)[0]
lines = re.findall(r'.+', html_body)
for n in range(20):
    print(lines[n])

# %%
driver.find_elements_by_tag_name('time')

# %%
for t in driver.find_elements_by_tag_name('time'):
    if t.get_attribute('id') != '':
        print(t.text)

# %% [markdown]
# ### Status Check
#
# https://cups.fast.ai/gitandweb

# %% [markdown]
# ### A slightly more advanced example
#
# Similar to web development, using Selenium for web scraping requires knowledge of HTML, CSS, and Javascript. One important skill to have is how to select elements from the document object model. There are various ways of identifying or selecting desired elements.
#
# Basic Tutorial on how the web works:
#
# https://www.freecodecamp.org/news/web-development-for-beginners-basic-html-and-css/
#
# And another:
#
# https://microsoft.github.io/Web-Dev-For-Beginners/
#
# Here are some references to learn more about Cascading Style Sheets aka CSS:
#
# * [The 30 CSS Selectors You Must Memorize](https://code.tutsplus.com/tutorials/the-30-css-selectors-you-must-memorize--net-16048)
# * [CSS Selector Reference](https://www.w3schools.com/cssref/css_selectors.asp)

# %%
driver.get('https://www.amazon.com')

# %%
search_box = driver.find_element_by_id('twotabsearchtextbox')
search_box.clear()
search_box.send_keys('512GB sd card\n')
search_box.submit()

# %% [markdown]
# Due to needing time for browser to load and render all content, if you run this next cell immediately after the previous one, it may fail.
#
# There are a few options to solve this issue:
#
# * Put in an explicit wait via `time.sleep()` call to help prevent problems.
# * Configure the driver to wait if an element found doesn't exist via `driver.implicitly_wait(n)`. In my experience with the Gecko driver, this can fail when chaining operations such as `li.find_element_by_class_name('a-link-normal').click()`
# * Depending on what is needed on a page, wait for that explicitly via `WebDriverWait(driver, n)`
#
# See https://selenium-python.readthedocs.io/waits.html for more information.

# %%
# Tell selenium to wait up to 5 seconds for desired elements to exist
driver.implicitly_wait(5)

# %%
# implicity_wait works here
dropdown = driver.find_element_by_class_name('a-dropdown-container')
time.sleep(2)
dropdown.click()
time.sleep(2)

# %%
# sort by 'Price: Low to High'
# implicity_wait often fails here
driver.find_element_by_id('s-result-sort-select_1').click()

# %%
# despite search terms, some small SDCards are shown
# click on the filter link on the left
li = driver.find_element_by_id('p_n_feature_two_browse-bin/13203835011')
li_class = li.find_element_by_class_name('a-link-normal')
li_class.click()

# %%
product_desc = []
product_price = []

products = driver.find_elements_by_css_selector('.sg-col.sg-col-4-of-12.sg-col-8-of-16.sg-col-12-of-20')
for p in products:
    product_desc.append(
        # product names/descriptions can be very long. just get first 50 characterss
        p.find_element_by_css_selector('.a-size-medium.a-color-base.a-text-normal').text[:50]
    )
    
    dollars = p.find_elements_by_class_name('a-price-whole')
    price = None
    if len(dollars) > 0:
        price = float(dollars[0].text)
    cents = p.find_elements_by_class_name('a-price-fraction')
    if len(cents) > 0:
        price = price + float('0.' + cents[0].text)
    product_price.append(price)

# %% [markdown]
# In order to build a dataframe from this information, both lists must be the same lenght. Check to make sure first

# %%
len(product_desc)

# %%
len(product_price)

# %%
pd.DataFrame({'product':product_desc,
              'price':product_price
              })

# %% [markdown]
# Note that although we selected sort by price, there are a few out of order items. That is the result of advertizements/sponsored products.
#
# ### Cleaning up
#
# When finished, make sure you close the browser. Can either `driver.quit()` or `driver.close()`. `.close()` will close open tabs. If you close the last tab, it is the same as calling `.quit()`

# %%
driver.quit()

# %%
try:
    driver.close()
except Exception:
    print('Already closed')

# %% [markdown]
# ### Status Check
#
# https://cups.fast.ai/gitandweb

# %% [markdown]
# ## Playwright Python binding
#
# "Modern successor to Selenium"
#
# https://playwright.dev/python/docs/intro
#
# Playwright can also create scripts interactively - you can then adjust or update later.
#
# ```bash
# playwright codegen wikipedia.org
# ```
#
# **Note:** The below code will not work in Jupyter on Windows OS. The code can be run directly via command line.

# %%
# Note - when running playwright inside Jupyter, special care must be taken due to existing Jupyter asynchronous code
# see https://github.com/microsoft/playwright-python/issues/178#issuecomment-680249269 for workarounds and alternatives
import nest_asyncio
nest_asyncio.apply()

import asyncio
from playwright.async_api import async_playwright

# %%
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        print(await page.title())
        await browser.close()

asyncio.run(main())

# %%
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://whatsmyuseragent.org/')
        await page.screenshot(path='playwright-ua.png')
        await browser.close()

asyncio.run(main())   

# %%
Image(filename='playwright-ua.png')

# %%
