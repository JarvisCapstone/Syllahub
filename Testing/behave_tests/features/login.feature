Feature: Login to Syllahub

  Scenario: go to Syllahub Home Page
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the browser title will contain Syllahub
     And    the page source will contain "Login"

  Scenario: we click on the Login link
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the page source will contain "Login"
     And    clicking on the link will navigate to jarvissyllahub.pythonanywhere.com/auth/login

