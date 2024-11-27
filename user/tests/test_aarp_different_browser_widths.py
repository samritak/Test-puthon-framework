import time
import pytest, sys
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpDifferentBrowserWidths:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - TEST DIFFERENT WIDTHS")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != "None":
            try:
                print("TESTING THE URL: " + base_url)
                self.perform_test_steps(base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - BROWSER WIDTH: {e}")
                # self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                # driver = self.common_functions.open_browser(url, Global_Env_Data.FIREFOX)
                # self.perform_test_steps(driver, url)
                # self.common_functions.close_browser(driver)
                try:
                    self.perform_test_steps(url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - BROWSER WIDTH: {e}")

    def perform_test_steps(self, url):
        print("PERFORM TEST BROWSER WIDTH CHANGE STEPS START")
        width = [375, 768, 1200, 1440]
        for index in width:
            print("SCREEN WIDTH: ", index)
            driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
            time.sleep(20)
            try:
                driver.delete_all_cookies()
                driver.set_window_size(index, height=800)
                self.full_page_screenshot_url = lambda x: driver.execute_script(
                    "return document.body.parentNode.scroll" + x
                )
                driver.set_window_size(
                    self.full_page_screenshot_url("Width"),
                    self.full_page_screenshot_url("Height"),
                )
                driver.find_element("tag name", "body").screenshot(
                    "user/static/reports/html/screenshot/page_load_screenshot_"
                    + url.split("/")[4]
                    + "_"
                    + str(index)
                    + ".png"
                )
                time.sleep(3)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - BROWSER WIDTH CHANGE: {e}")
            finally:
                self.common_functions.close_browser(driver)
        print("verified page in different widths - 375, 768, 1200, 1440")
        print("PERFORM TEST BROWSER WIDTH CHANGE STEPS END")
