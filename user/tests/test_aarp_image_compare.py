import time, pytest, sys

from user.tests.common_functions import TestCommonFunctions
from selenium.webdriver.common.by import By


class TestAarpImageCompare:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE Image comparison begins")
        self.common_functions = TestCommonFunctions()
        # image_url = sys.argv[2].split("--base-url=")[1]
        image_url = "https://www.aarp.org/membership/bc5-pyp-calc-summer-travel/"
        print(image_url)
        if image_url != "None":
            try:
                print("TESTING THE URL: " + image_url)
                # driver = self.common_functions.open_browser(image_url, Global_Env_Data.CHROME)
                # self.perform_test_steps(driver, image_url)
                # self.common_functions.run_image_compare(image_url)
                print("Hello beginning")
                #
                driver = self.common_functions.open_browser(image_url, "Firefox")
                time.sleep(10)
                self.common_functions.take_screenshot(driver)
                time.sleep(15)
                self.common_functions.image_compare()
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - Category Level Accord: {e}")
            finally:
                self.common_functions.close_browser(driver)
