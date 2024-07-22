Feature: Testing the Create endpoint
#
#
  Scenario Outline: Register a new person
    When I send a authenticated POST request to /api/register with <data>
    Then the status code is 400
    And The body will contain correct response for <data_validation>
    Examples:
      | data                     | data_validation |
      | base_data                | PostRegister    |
#      | base_data without: email | PostRegister    |  Needs to be implemented ( FIX data_string_parser )

