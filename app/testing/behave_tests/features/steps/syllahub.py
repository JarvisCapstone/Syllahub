from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

@given(u'we are browsing jarvissyllahub.pythonanywhere.com/')
def step_impl(context):
    browser = webdriver.Chrome()
    context.browser = browser 
    browser.get("https://jarvissyllahub.pythonanywhere.com")
    #time.sleep(5)
    assert 'Syllahub' in browser.page_source

@then(u'we should see \"Syllahub\"')
def step_impl(context):
    browser = context.browser
    assert 'Syllahub.' in browser.page_source

#add further steps here in one long sequence
