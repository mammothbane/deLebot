# Created by mammothbane at 3/20/2015
Feature: Download source from Valve
  Want to ensure we connect to Valve's server
  and that the page still exists in the format we expect it to

  Scenario: GET Request
    When we send a GET to the server
    Then we should receive a 200 ok
    And the response should be html