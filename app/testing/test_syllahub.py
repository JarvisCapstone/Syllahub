from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()
try:
    browser.get("http://jarvissyllahub.pythonanywhere.com/")
    assert "Syllahub" in browser.title

    search = browser.find_element_by_id("searchbox") #need to add this id to input
    search.clear()
    search.send_keys("test")
    search.send_keys(Keys.RETURN)
    assert "No results found." not in browser.page_source
    #time.sleep(5)

finally:
    browser.close()

'''
#old stuff
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def test_register_submits_data_into_db():
    browser = webdriver.Chrome()
    browser.get(url + "/")
    #assert "No results found." not in browser.page_source
    time.sleep(10)
    browser.close()
    
def test_login_verifies_data_from_db():
    browser = webdriver.Chrome()
    browser.get(url + "/")
    time.sleep(10)
    browser.close()
'''
