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
    # the tests running in parallel in a BrowserStack instance;
    # To get them to run parallel, uncomment the following 9 lines and comment
    # line 33

    # desired_cap = []
    # desired_cap.append({'os': 'OS X', 'os_version': 'Sierra', 'browser': 'Chrome', 'browser_version': '54.0' })
    # desired_cap.append({'browserName': 'iPhone', 'platform': 'MAC', 'device': 'iPhone 6S Plus'})
    # desired_cap.append({'browserName': 'android', 'platform': 'ANDROID', 'device': 'Samsung Galaxy S5'})
    # for driver_instance in desired_cap:
    #         driver_instance['browserstack.debug'] = True
    #         context.driver = webdriver.Remote(
    #         command_executor='http://cristianivan1:LSHUqy4qiydc9N8kkVnv@hub.browserstack.com:80/wd/hub',
    #         desired_capabilities=driver_instance)
    try:
        context.driver.maximize_window()
    except:
        pass
    context.driver = webdriver.Chrome(executable_path="features/driver/chromedriver")

def before_scenario(context, scenario):
    context.driver.delete_all_cookies()

def after_all(context):
    context.driver.quit()
