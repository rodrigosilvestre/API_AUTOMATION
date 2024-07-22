Feature: Testing the Create endpoint


  Scenario Outline: Create a new user
    When I send a authenticated POST request to /api/users with <data>
    Then the status code is 201
    And The body will contain correct response for <data_validation>
    Examples:
      | data                            | data_validation |
      | base_data                       | PostUser         |
      | optional_data                   | PostUser         |
#      | base_data with: name as Rodrigo | user, created   |
#      | base_data with: job as QA       | user, created   |

  Scenario: Retrieve users from page
    When I send a authenticated GET request to /api/users?page=2
    Then The status code is 200
    And The body will contain correct response for GetUser

  Scenario: Retrieve users from ID
    Given I have a new base_data from /api/users
    When I send a authenticated GET request to /api/users/{user_id}
    Then The status code is 200
    And The body will contain correct response for GetUser
