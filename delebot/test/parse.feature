# Created by mammothbane at 3/22/2015
Feature: Parse html for pertinent elements

  Scenario: We get the html we expect from the server
    When the server sends us a valid html document
    Then we parse it without errors