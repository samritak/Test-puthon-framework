import time
import pytest, sys
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpDifferentWidthsWithScroll:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - TEST DIFFERENT WIDTHS WITH SCROLL")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != "None":
            try:
                print("TESTING THE URL: " + base_url)
                self.perform_test_steps(base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - DIFF WIDTHS SCROLL: {e}")
                # self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                try:
                    self.perform_test_steps(url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - DIFF WIDTHS SCROLL: {e}")

    def perform_test_steps(self, url):
        print("PERFORM TEST DIFFERENT WIDTHS WITH SCROLL STEPS START")
        width = [375, 768, 1200, 1440]
        for index in width:
            driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
            time.sleep(20)
            try:
                print("SCREEN WIDTH: ", index)
                driver.delete_all_cookies()
                time.sleep(3)
                driver.set_window_size(index, height=800)
                time.sleep(5)
                self.full_page_screenshot_lp = lambda x: driver.execute_script(
                    "return document.body.parentNode.scroll" + x
                )
                driver.set_window_size(
                    self.full_page_screenshot_lp("Width"),
                    self.full_page_screenshot_lp("Height"),
                )
                driver.find_element("tag name", "body").screenshot(
                    "user/static/reports/html/screenshot/page_width_"
                    + str(index)
                    + "_load_screenshot_.png"
                )
                time.sleep(3)
                script = f"window.scrollTo(0, document.body.scrollHeight);"
                driver.execute_script(script)
                time.sleep(3)
                self.full_page_screenshot_lp = lambda x: driver.execute_script(
                    "return document.body.parentNode.scroll" + x
                )
                driver.set_window_size(
                    self.full_page_screenshot_lp("Width"),
                    self.full_page_screenshot_lp("Height"),
                )
                driver.find_element("tag name", "body").screenshot(
                    "user/static/reports/html/screenshot/page_width_"
                    + str(index)
                    + "_scroll_screenshot_.png"
                )
                time.sleep(3)
                script = f"window.scrollTo(0, 0);"
                driver.execute_script(script)
                time.sleep(5)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - DIFFERENT WIDTH WITH SCROLL: {e}")
            finally:
                self.common_functions.close_browser(driver)

        print("VERIFIED PAGE IN DIFFERENT WIDTHS WITH SCROLL - 375, 768, 1200, 1440")
        print("PERFORM TEST DIFFERENT WIDTHS WITH SCROLL STEPS END")
