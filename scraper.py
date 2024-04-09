from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set the path to the WebDriver executable. Here I'm using Chrome WebDriver.
# You need to download the WebDriver executable compatible with your browser version.
# For Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
driver_path = '/path/to/chromedriver'

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Open the login page of Nairaland
driver.get('https://www.nairaland.com/login')

# Find the username and password input fields and fill them out
username_input = driver.find_element('name','login')
password_input = driver.find_element('name','password')

username_input.send_keys('beodw')
password_input.send_keys('Password123')

# Submit the form
password_input.send_keys(Keys.RETURN)


# Wait for at least 10 seconds before exiting
time.sleep(10)

politics_forum_link = driver.find_element('href','/politics')


politics_forum_link.send_keys(Keys.RETURN)
time.sleep(10)


# Close the browser
# driver.quit()
