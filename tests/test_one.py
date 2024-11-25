from flask import Flask
from user.controllers import browser_controller
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

# Test One
def execute_test_one():
   driver = browser_controller.init()
   browser_controller.open("www.google.com")
   search_box = driver.find_element("name", "q")
   time.sleep(2)
   search_box.clear()
   search_box.send_keys("Python")
   search_box.send_keys(Keys.ENTER)
   time.sleep(2)
   title = driver.find_element(By.TAG_NAME, "title").get_attribute("textContent");
   print(title)
   browser_controller.close()
   return "Test One is executed successfully ";