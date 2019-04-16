Feature: Syllahub search capability

  Scenario: go to Syallhub Home Page
    Given   we have a Chrome browser
    When    we navigate to jarvissyllahub.pythonanywhere.com
    Then    the browser title will contain Syllahub

  Scenario: Search for a "user"
    Given   We are at jarvissyllahub.pythonanywhere.com
    When    we search for "test"
    Then    we will get at least 1 result
     And    100% of the results will contain "test"

  Scenario: Search for a "instructor"
    Given   We are at jarvissyllahub.pythonanywhere.com
    When    we search for "samba"
    Then    we will get at least 1 result
     And    100% of the results will contain "samba"

  Scenario: Search for a "course"
    Given   We are at jarvissyllahub.pythonanywhere.com
    When    we search for "capstone"
    Then    we will get at least 1 result
     And    100% of the results will contain "capstone"

  Scenario: Search for a "syllabus"
    Given   We are at jarvissyllahub.pythonanywhere.com
    When    we search for "spring2019"
    Then    we will get at least 1 result
     And    100% of the results will contain "spring2019"
    