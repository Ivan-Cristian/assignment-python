from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import logging


def before_all(context):
    selenium_logger = logging.getLogger(
        'selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.INFO)
    context.base_url = "https://preview.debijenkorf.nl"

    # currently, the system is set up to run on local Chrome browser;
    # I haven't found a more elegant solution, though it is possible, to get
    # the tests running in parallel in a BrowserStack instance; the way to get
    # them running in different browsers on different OS is to comment line 30
    # and then uncomment the desired_cap (either line 20, 21 or 22) as well as
    # lines 23-25; this will run the tests in BrowserStack with the specified settings

    # desired_cap = {'os': 'OS X', 'os_version': 'Sierra', 'browser': 'Chrome', 'browser_version': '54.0' }
    # desired_cap = {'browserName': 'iPhone', 'platform': 'MAC', 'device': 'iPhone 6S Plus'}
    # desired_cap = {'browserName': 'android', 'platform': 'ANDROID', 'device': 'Samsung Galaxy S5'}
    # context.driver = webdriver.Remote(
    # command_executor='http://cristianivan2:mKQpf6t7yGpXzd1T5Bek@hub.browserstack.com:80/wd/hub',
    # desired_capabilities=desired_cap)
    try:
        context.driver.maximize_window()
    except:
        pass
    context.driver = webdriver.Chrome(executable_path="features/driver/chromedriver")


def before_scenario(context, scenario):
    context.driver.delete_all_cookies()

def after_all(context):
    context.driver.quit()
