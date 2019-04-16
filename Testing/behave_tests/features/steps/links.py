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

@And(u'the navbar will contain "Login"')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Login" in _browser.page_source 

@And(u'the navbar will contain "Register"')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Register" in _browser.page_source

@given(u'we are at jarvissyllahub.pythonanywhere.com')
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get("https://jarvissyllahub.pythonanywhere.com")
    assert "syllahub" in context.browser.title.lower()

@when(u'we click on the login link')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    #_browser.get("https://jarvissyllahub.pythonanywhere.com")
    #assert

@when(u'the browser title will contain Login')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Login" in _browser.title

@given(u'we are at jarvissyllahub.pythonanywhere.com')
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get("https://jarvissyllahub.pythonanywhere.com")
    assert "syllahub" in context.browser.title.lower()

@when(u'we click on the register link')
def step_impl(context):
    global _browser
    #assert

@when(u'the browser title will contain Register')
def step_impl(context):
    global _browser
    #_browser = webdriver.Chrome()
    assert "Register" in _browser.title
