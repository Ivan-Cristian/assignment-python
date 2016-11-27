from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import logging


def before_all(context):
    selenium_logger = logging.getLogger(
        'selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.INFO)
    context.base_url = "https://preview.debijenkorf.nl"
    item_id = str(float(time.time()))
    context.item_name = 'Test Item {item_id}'.format(item_id=item_id)
    desired_cap = {'os': 'OS X', 'os_version': 'Sierra', 'browser': 'Chrome', 'browser_version': '54.0' }
    context.driver = webdriver.Remote(
    command_executor='http://cristianivan2:mKQpf6t7yGpXzd1T5Bek@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)



    # context.driver = webdriver.Chrome(executable_path="/Users/cristian/Downloads/chromedriver")

    context.driver.maximize_window()

def before_scenario(context, scenario):
    context.driver.delete_all_cookies()

def after_all(context):
    context.driver.quit()
