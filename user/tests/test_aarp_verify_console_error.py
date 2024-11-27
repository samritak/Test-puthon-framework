import time, pytest, sys

from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpVerifyConsoleError:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - AARP CONSOLE ERROR")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != "None":
            try:
                print("TESTING THE URL: " + base_url)
                driver = self.common_functions.open_browser(
                    base_url, Global_Env_Data.CHROME
                )
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - CONSOLE ERROR: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(5)
                try:
                    self.perform_test_steps(driver, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - CONSOLE ERROR : {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("PERFORM CONSOLE ERROR TEST STEPS START")
        # self.full_page_screenshot_lp = lambda x: driver.execute_script('return document.body.parentNode.scroll' + x)
        # driver.set_window_size(self.full_page_screenshot_lp('Width'),
        # self.full_page_screenshot_lp('Height'))  # May need manual adjustment
        # #driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot_' + url.split('/')[4] + '.png')
        time.sleep(5)
        print("verified the list of console error in the page")
        entries = driver.get_log("browser")
        error_msgs = []
        for entry in entries:
            if entry["level"] == "SEVERE":
                error_msgs.append(entry["message"])
        print(error_msgs)

        if len(error_msgs) > 0:
            self.send_mail_cta(self, driver, str(error_msgs), url)
        print("PERFORM CONSOLE ERROR TEST STEPS ENDS")

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Verify Console Error"
        body = "Error: " + error_message + " \nURL: " + url
        common_functions.send_email(subject, body)
