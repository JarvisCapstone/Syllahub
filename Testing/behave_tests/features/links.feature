Feature: Navigate through Syllahub

  Scenario: go to Syllahub Home Page
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the browser title will contain Syllahub
     And    the navbar will contain "Login"
     And    the navbar will contain "Register"

  Scenario: Click on the login link
    Given   we are at jarvissyllahub.pythonanywhere.com
    When    we click on the login link
    Then    the page title will contain Login

  Scenario: Click on the register link
    Given   we are at jarvissyllahub.pythonanywhere.com
    When    we click on the register link
    Then    the page title will contain Register
