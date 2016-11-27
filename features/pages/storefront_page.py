from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import re

class StorefrontPage(BasePage):
    _bijkorf_logo = (By.XPATH, '//div/a[@class="dbk-header--logo"]')
    _search_bar = (By.XPATH, '//form/input[@type="search"]')

    def visit_page(self, context):
        context.driver.get(context.base_url)
        # on loading the page, check that the logo is displayed
        self.wait_for_element_to_appear(context, self._bijkorf_logo)
        return StorefrontPage()

    def search_for_product(self, context, product):
        self.find_element(context, self._search_bar).send_keys(product)
        self.find_element(context, self._search_bar).send_keys(Keys.ENTER)
        return SearchResultsPage(context)

class SearchResultsPage(BasePage):
    _search_results_header = (By.XPATH, '//h1/span[contains(@class, "lbl-search-term")]')

    def __init__(self, context):
        self.element_is_present(context, self._search_results_header)

    def select_result_number(self, context, number):
        # reusable method to select a search result based on its number in the list
        result_number = (By.XPATH, '//ul[@data-dbk-productlist="plp"]/li[{number}]'.format(number=number))
        self.find_element(context, result_number).click()
        return ProductDetailsPage(context)

class ProductDetailsPage(BasePage):
    _variant_dropdown = (By.XPATH, '//div/select[@class="dbk-form--input"]')
    _add_to_cart = (By.XPATH, '//div/button[contains(text(), "in winkelmand")]')
    _notification_panel = (By.CLASS_NAME, 'dbk-notification--message')
    _shopping_bag = (By.XPATH, '//*[@class="hidden-xs"][@title="Shopping basket"]')
    _basket_slidein = (By.XPATH, '//*[@data-dbk-account-bag-trigger][contains(text(), "bestellen")]')
    _cart_product = (By.XPATH, '//h1[@class="dbk-heading dbk-heading_brand dbk-heading_h2 hidden-xs"]')
    _slidein_product_title = (By.XPATH, '//h1/a')

    def __init__(self, context):
        self.element_is_present(context, self._add_to_cart)

    def select_variant(self, context, text):
        # will select a variant of the product based on the text displayed in the dropdown
        Select(self.find_element(context, self._variant_dropdown)).select_by_visible_text(text)
        return ProductDetailsPage(context)

    def add_product_to_cart(self, context):
        self.scroll_into_view(context, self._add_to_cart)
        self.find_element(context, self._add_to_cart).click()
        # verify that the product was added to cart by confirming the message first
        self.wait_for_text_to_be_present\
            (context, self._notification_panel,
            "Dit artikel is toegevoegd aan uw winkelmand")
        return ProductDetailsPage(context)

    def verify_product_was_added_to_cart(self, context):
        product_title = self.get_element_text(context, self._cart_product)
        try:
            # click on the shopping cart
            self.find_element(context, self._shopping_bag).click()
        except WebDriverException:
            # if the confirmation panel from adding the product to cart is still
            # present, this will catch the error and wait for it to disappear
            # before attempting to click again
            # TODO: find a way to parse exception message and grab class name from it
            self.wait_for_element_to_disappear(context, self._notification_panel)
            self.scroll_into_view(context, self._shopping_bag)
            self.find_element(context, self._shopping_bag).click()
        # wait for the slidein to appear, then assert that the product I was
        # viewing is the product present in the cart
        self.wait_for_element_to_appear(context, self._basket_slidein)
        assert product_title in self.get_element_text(context, self._slidein_product_title)
