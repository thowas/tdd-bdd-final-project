Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description     | price   | available | category   |
        | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
        | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
        | Burger    | 1/4 lb burger   | 5.99    | True      | FOOD       |
        | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I select "True" in the "Available" dropdown
    And I select "Tools" in the "Category" dropdown
    And I set the "Price" to "34.95"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field

Scenario: Update a Product
    Given I create a product with
    | name     | description | price | available | category |
    | Hammer   | Claw hammer | 34.95 | True      | Tools    |
   
    And I store the product id

    When I click the "Clear" button
    And I enter the stored product id
    And I click the "Retrieve" button
    Then I should see the message "Success"

    When I change the "price" to "79.95"
    And I click the "Update" button
    Then I should see the message "Success"

    When I click the "Clear" button
    And I enter the stored product id
    And I click the "Retrieve" button
    Then I should see the message "Success"
    And the "price" field should contain "79.95"

Scenario: Reading a product
    Given I create a product with
    | name     | description | price | available | category |
    | Hammer   | Claw hammer | 34.95 | True      | Tools    |

    And I store the product id
    When I click the "Clear" button
    And I enter the stored product id
    And I click the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Hammer" in the "Name" field
    And I should see "Claw hammer" in the "Description" field
    And I should see "True" in the "Available" dropdown
    And I should see "Tools" in the "Category" dropdown
    And I should see "34.95" in the "Price" field


Scenario: Deleting a Product
    When I visit the "Home Page"
    And I clear the form
    Given I create a product with
    | name     | description | price | available | category |
    | Saw      | Power tool  | 49.99 | True      | Tools    |
    Then I should see the message "Success"
    Then I store the product id

    When I clear the form
    And I enter the stored product id
    And I click the "Delete" button
    Then I should see the message "Product has been Deleted!"

    When I clear the form
    And I enter the stored product id
    And I click the "Retrieve" button
    Then the product should no longer exist

Scenario: LISTING ALL
    When I visit the "Home Page"
    Given I create a product with
    | name     | description | price | available | category |
    | Burger   | Big Mac     | 5.99  | True      | Food     |
    | Fanta    | Orange soda | 2.49  | True      | Food     |
    | Keyboard | Mechanical  | 29.90 | True      | Tools    |

    When I click the "Clear" button
    And I click the "Search" button
    Then I should see "Burger" in the search results
    And I should see "Fanta" in the search results
    And I should see "Keyboard" in the search results

Scenario: Search products by category
    Given the following category
    | name     | description | price | available | category |
    | Burger   | Big Mac     | 5.99  | True      | Food     |
    | Fanta    | Orange soda | 2.49  | True      | Food     |
    | Keyboard | Mechanical  | 29.90 | True      | Tools    |
    When I click the "Clear" button
    And I select "Food" in the "category" dropdown
    And I click the "Search" button
    Then I should see "Burger" in the search results
    And I should see "Fanta" in the search results
    And I should not see "Keyboard" in the search results

Scenario: Search products by availability

    When I select "True" in the "Available" dropdown
    And I click the "Search" button
    Then I should see only products where availability is True in the results