import datetime
import os
import ssl
import time
from ssl import SSLContext
import smtplib
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#import chromedriver_autoinstaller
#import geckodriver_autoinstaller
from selenium import webdriver

"""
This fixture we use for initialization of the driver. We use this through out project.
"""
driver = None

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    date_time = datetime.datetime.now()
    unix_timestamp = formatNumber(time.mktime(date_time.timetuple()))
    report_file_name = str(unix_timestamp)
    file_name = report_file_name + ".png"
    if report.when == "call":
        file_list = os.listdir("user/static/reports/html/screenshot/")
        print(file_list)
        if file_name:
            for file in file_list:
                screenshot_path = "../html/screenshot/" + file
                if file:
                    onload_screenshot = '<div style="clear:both;"><img src="%s" alt="screenshot" style="width: 384px;height: auto;" onclick="window.open(this.src)" align="right" /></div>' % screenshot_path
                    extra.append(pytest_html.extras.html(onload_screenshot))
        # always add url to report
        xfail = hasattr(report, "wasxfail")
        # if file_name:
        #     file_path1 = "screenshot/onload_screenshot.png"
        #     if file_path1:
        #         onload_screenshot = '<div style="clear:both;"><img src="%s" alt="screenshot" style="width: 384px;height: auto;" onclick="window.open(this.src)" align="right" /></div>' % file_path1
        #         extra.append(pytest_html.extras.html(onload_screenshot))

            # file_path2 = "screenshot/application_page.png"
            # if file_path2:
            #     after_test_screenshot = '<div style="clear:both;"><img src="%s" alt="screenshot" style="width: 384px;height: auto;" onclick="window.open(this.src)" align="right" /></div>' % file_path2
            #     extra.append(pytest_html.extras.html(after_test_screenshot))


def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

# @pytest.fixture(autouse=True)
# def init_driver(request, binary=None, options=None):
#     global web_driver
#     web_driver = webdriver.Firefox()
#     request.cls.driver = web_driver
#     yield
#     web_driver.quit()

@pytest.fixture(autouse=False)
def init_driver(request, binary=None, options=None):
    global web_driver
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    #options.add_argument("--incognito")
    #options.add_argument(
    ##'--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    #web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='118.0.5993.71').install()), options=options))
    web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    request.cls.driver = web_driver
    yield
    #web_driver.quit()

def pytest_html_report_title(report):
    report.title = "AARP Report"

def pytest_html_results_table_header(cells):
	''' meta programming to modify header of the result'''

	from py.xml import html
	# removing old table headers
	del cells[:]
	# adding new headers
	cells.insert(0, html.th('Result'))
	cells.insert(1, html.th('Test'))
	cells.insert(2, html.th('Duration'))
	cells.insert(3, html.th('Screenshot'))

# Set fixture to captire tests to be executed from input
def pytest_addoption(parser):
    parser.addoption(
        "--inputtests",
        action="append",
        default=[]
    )
