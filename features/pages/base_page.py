from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import WebDriverException
import re

class BasePage(object):
# base page contains all the methods that can be used in the page object files
# it's just a wrapper around some selenium calls, but it makes it makes the code
# cleaner and easier to understand

    def element_is_present(self, context, locator):
        WebDriverWait(context.driver, 15).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_text_to_be_present(self, context, locator, text):
        WebDriverWait(context.driver, 15).until(
            EC.text_to_be_present_in_element(locator, text)
            )

    def scroll_into_view(self, context, to_element):
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(context.driver).move_to_element(to_element)
        # self._driver = context.driver
        # self._actions = []
        # self._actions.append(lambda: self._driver.execute(
        #     Command.MOVE_TO, {'element': to_element.id}))
        return self

    def wait_for_element_to_disappear(self, context, locator):
        WebDriverWait(context.driver, 15).until(
            EC.invisibility_of_element_located(locator)
        )
    def find_by_text(self, context, text):
        return context.driver.find_element(By.XPATH, '//*[contains(text(), "{text}")]'.format(text=text))


    def wait_for_element_to_appear(self, context, locator):
        WebDriverWait(context.driver, 15).until(
            EC.visibility_of_element_located(locator)
        )

    def get_element_text(self, context, element):
        return context.driver.find_element(*element).text

    def find_element(self, context, element):
        self.element_is_present(context, element)
        return context.driver.find_element(*element)
