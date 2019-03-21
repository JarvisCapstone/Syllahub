import requests
from bs4 import BeautifulSoup

url = "http://jarvissyllahub.pythonanywhere.com"

def test_home_page():
    response = requests.get(url + "/")
    assert response.status_code == 200
    assert response.text > ""
    assert "Syllahub" in response.text

def test_home_page_has_login_and_register():
    response = requests.get(url + "/")
    assert response.status_code == 200
    assert "href=\"/auth/login\"" in response.text.lower().replace(" ","")
    assert "href=\"/auth/register\"" in response.text.lower().replace(" ","")
            
def test_home_search_bar():
    response = requests.get(url + "/")
    assert response.status_code == 200
    assert "type=\"search\"" in response.text.lower().replace(" ","")
    #need to later enter something, click on it, verify result
    soup = BeautifulSoup(response.text,"html.parser")
    inputs = soup.find_all("input")
    submit_inputs = [ input for input in inputs if input['type'] == "submit" ]
    assert len(submit_inputs) > 0
    for input in submit_inputs:
        assert input["value"] == "Submit"

def test_login_page():
    response = requests.get(url + "/auth/login")
    assert response.status_code == 200
    assert response.text > ""
    assert "login" in response.text

def test_register_page():
    response = requests.get(url + "/auth/register")
    assert response.status_code == 200
    assert response.text > ""
    assert "register" in response.text

def test_login_page_submit_button():
    response = requests.get(url + "/auth/login")
    assert response.status_code == 200
    assert "type=\"submit\"" in response.text.lower().replace(" ","")
    soup = BeautifulSoup(response.text,"html.parser")
    inputs = soup.find_all("input")
    submit_inputs = [ input for input in inputs if input['type'] == "submit" ]
    assert len(submit_inputs) > 0
    for input in submit_inputs:
        assert input["value"] == "Submit"

def test_register_page_submit_button():
    response = requests.get(url + "/auth/register")
    assert response.status_code == 200
    assert "type=\"submit\"" in response.text.lower().replace(" ","")
    soup = BeautifulSoup(response.text,"html.parser")
    inputs = soup.find_all("input")
    submit_inputs = [ input for input in inputs if input['type'] == "submit" ]
    assert len(submit_inputs) > 0
    for input in submit_inputs:
        assert input["value"] == "Submit"
