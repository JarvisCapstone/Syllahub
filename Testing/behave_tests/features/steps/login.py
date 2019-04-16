from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

_browser = None

@given(u'we have a Chrome browser')
def step_impl(context):
    global _browser
    _browser = webdriver.Chrome()
    assert _browser

@when(u'we navigate to jarvissyllahub.pythonanywhere.com')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    _browser.get("https://jarvissyllahub.pythonanywhere.com")

@then(u'the browser title will contain Syllahub')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Syllahub" in _browser.title

@And(u'the page source will contain "Login"')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Login" in _browser.page_source

#and clicking on login takes you to jarvissyllahub.pythonanywhere.com/auth/login
