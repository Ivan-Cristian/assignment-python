from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidElementStateException
from selenium.common.exceptions import TimeoutException
import re

class StorefrontPage(BasePage):
    _bijkorf_logo = (By.XPATH, '//div/a[@class="dbk-header--logo"]')
    _search_bar = (By.XPATH, '//form/input[@type="search"]')
    _search_bar_mobile = (By.XPATH, '//*[@class="dbk-ocp-nav--wrap dbk-off-canvas-pane--slider"]/div/div/section/div/form/input')
    _mobile_menu = (By.XPATH, '//*[@data-dbk-off-canvas-pane-toggle="dbk-ocp-nav"]')
    _close_cookie_bar = (By.XPATH, '//div[@class="dbk-cookiebar"]/div/button')

    def visit_page(self, context):
        context.driver.get(context.base_url)
        # on loading the page, check that the logo is displayed
        self.wait_for_element_to_appear(context, self._bijkorf_logo)
        self.wait_for_element_to_appear(context, self._close_cookie_bar)
        self.find_element(context, self._close_cookie_bar).click()
        return StorefrontPage()

    def search_for_product(self, context, product):
        try:
            self.find_element(context, self._search_bar).send_keys(product)
            self.find_element(context, self._search_bar).send_keys(Keys.ENTER)
            return SearchResultsPage(context)
        except InvalidElementStateException:
            # mobile version returns multiple elements with same ID
            # workaround is to open the menu and use the searchbar there
            self.find_element(context, self._mobile_menu).click()
            self.wait_for_element_to_appear(context, self._search_bar_mobile)
            self.find_element(context, self._search_bar_mobile).click()
            self.find_element(context, self._search_bar_mobile).send_keys(product)
            self.find_element(context, self._search_bar_mobile).send_keys(Keys.ENTER)
            return SearchResultsPage(context)

class SearchResultsPage(BasePage):
    _search_results_header = (By.XPATH, '//h1/span[contains(@class, "lbl-search-term")]')

    def __init__(self, context):
        self.element_is_present(context, self._search_results_header)

    def select_result_number(self, context, number):
        # reusable method to select a search result based on its number in the list
        try:
            result_number = (By.XPATH, '//*[@class="dbk-productlist--item"][{number}]'.format(number=number))
            self.scroll_into_view(context, result_number)
            self.find_element(context, result_number).click()
            return ProductDetailsPage(context)
        except TimeoutException:
            self.scroll_into_view(context, result_number)
            # seems like the livechat and feedback elements are interfering with
            # with the click on mobile, sending a script to set those elements
            # to hidden and try to click on the CSS selector
            elem = context.driver.find_element(By.ID, 'livechat-compact-view');
            elem2 = context.driver.find_element(By.ID, 'livechat-badge');
            js = "arguments[0].style.height='auto'; arguments[0].style.visibility='hidden';";
            context.driver.execute_script(js, elem);
            context.driver.execute_script(js, elem2);
            elem2 = context.driver.find_element(By.CLASS_NAME, 'usabilla_live_button_container')
            # last resort
            self.find_element(context, (By.CSS_SELECTOR, 'li:nth-child({number}) > div > a'\
                .format(number=number))).click()
            return ProductDetailsPage(context)


class ProductDetailsPage(BasePage):
    _variant_dropdown = (By.XPATH, '//div/select[@class="dbk-form--input"]')
    _add_to_cart = (By.XPATH, '//div/button[contains(text(), "in winkelmand")]')
    _notification_panel = (By.CLASS_NAME, 'dbk-notification--message')
    _shopping_bag = (By.XPATH, '//*[@class="hidden-xs"][@title="Shopping basket"]')
    _shopping_bag_mobile = (By.XPATH, '//*[@class="visible-xs"][@title="Shopping basket"]')
    _basket_slidein = (By.XPATH, '//*[@data-dbk-account-bag-trigger][contains(text(), "bestellen")]')
    _cart_product = (By.XPATH, '//h1[@class="dbk-heading dbk-heading_brand dbk-heading_h2 hidden-xs"]')
    _slidein_product_title = (By.XPATH, '//h1/a')
    _slidein_mobile = (By.XPATH, '//h3[@class="dbk-heading dbk-heading--brand dbk-heading_h4"]')

    def __init__(self, context):
        self.element_is_present(context, self._add_to_cart)

    def select_variant(self, context, text):
        # will select a variant of the product based on the text displayed in the dropdown
        self.scroll_into_view(context, self._variant_dropdown)
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
            self.wait_for_element_to_appear(context, self._basket_slidein)
            assert product_title in self.get_element_text(context, self._slidein_product_title)
        except WebDriverException:
            # if the confirmation panel from adding the product to cart is still
            # present, this will catch the error and wait for it to disappear
            # before attempting to click again
            try:
                self.wait_for_element_to_disappear(context, self._notification_panel)
                self.scroll_into_view(context, self._shopping_bag)
                self.find_element(context, self._shopping_bag).click()
                self.wait_for_element_to_appear(context, self._basket_slidein)
                assert product_title in self.get_element_text(context, self._slidein_product_title)
            except TimeoutException:
                self.find_element(context, self._shopping_bag_mobile).click()
                self.wait_for_element_to_appear(context, self._slidein_mobile)
                assert product_title in self.get_element_text(context, self._slidein_mobile)
