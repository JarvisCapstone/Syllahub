Feature: Register with Syllahub

  Scenario: go to Syllahub Home Page
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the browser title will contain Syllahub
     And    the page source will contain "Register"

  Scenario: we click on the Register link
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the page source will contain "Register"
     And    clicking on the link will navigate to jarvissyllahub.pythonanywhere.com/auth/register
