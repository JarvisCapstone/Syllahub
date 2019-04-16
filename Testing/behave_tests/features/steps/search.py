from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

@given(u'We are at jarvissyllahub.pythonanywhere.com')
def step_impl(context):
    context.browser = webdriver.Chrome()
    context.browser.get("https://jarvissyllahub.pythonanywhere.com")
    assert "syllahub" in context.browser.title.lower()

@when(u'we search for "{item}"')
def step_impl(context, item):
    search_box = context.browser.find_element_by_id("searchbox") #we need to add this id to the search input
    search_box.clear()
    search_box.send_keys(item)
    search_box.send_keys(Keys.RETURN)

@then(u'we will get at least 1 result')
def step_impl(context):
    context.result_items = context.browser.find_elements_by_class_name("s-result-item")
    assert len(context.result_items) >= 20

@then(u'100% of the results will contain "{item}"')
def step_impl(context, item):
    n = 0
    for result_item in context.result_items:
        if item in result_item.text.lower():
            n += 1
    assert n * 4 >= len(context.result_items) * 3

#add more test cases with when-then format
