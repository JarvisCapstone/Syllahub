from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

browser = webdriver.Chrome()
browser.get("http://localhost:5000")
assert "Web Browser: " in browser.title

instructor_usernames = browser.find_element_by_name("Username")
print(len(instructor_usernames))