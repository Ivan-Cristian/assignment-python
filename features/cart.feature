Feature: Cart

@cart
Scenario Outline: Add product to cart
Given I am at the storefront
When I search for <product>
And I select the second result
And I change the selected variant
Then I can add the product to the Cart
Examples:
|product|
|jeans|
