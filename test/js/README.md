# Using MochaJS and Selenium WebDriver to Test the TolaActivity UI

This document describes setting up and testing Selenium WebDriver
for Python and the Chrome browser. If you're using Python, you
can install using `pip` (this should work for either Python 2 or
Python 3 -- use Python 3 if you have a choice).

## Install Things
1. Download Selenium language bindings and browser driver(s) for the
language(s) you want to use and the browsers you want to test.
```
$ pip install selenium-webdriver
```
1. Download the chromedriver from Google Code:
https://sites.google.com/a/chromium.org/chromedriver/.
and place it anywhere in your system PATH.

1. If you're using Javascript, install Node.js so you can use `npm` (the
Node Package Manager). It won't be necessary to install the JavaScript
language bindings. Installing Node installs the `npm` package manager,
which in turn you can use to install other JavaScript packages you
might need.

OPTIONAL: Although not necessary, because MC does not use Node, you
can install the JavaScript language bindings like so:
```
$ npm install selenium-webdriver
```

## Validate the Python Driver Installation

Use the following Python 2 code to validate that the driver is installed
and working properly:
```
import time
from selenium import webdriver

driver = webdriver.Chrome('/Users/kwall/bin/chromedriver')
driver.get('http://www.google.com')
time.sleep(2)
element = driver.find_element_by_name('q')
element.sendKeys('Mercy Corps')
time.sleep(2)
driver.quit()
```

