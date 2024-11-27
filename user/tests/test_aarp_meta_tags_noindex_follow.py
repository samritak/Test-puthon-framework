import ssl
import smtplib
import pytest, sys, time
from user.Config.config import Global_Env_Data
from email.message import EmailMessage
from user.tests.common_functions import TestCommonFunctions


class TestAarpMetaTagsNoindexFollow:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - AARP PAGE META TAGS NOINDEX FOLLOW")
        text_to_find = Global_Env_Data.NOINDEX_FOLLOW
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
                self.perform_test_steps(driver, text_to_find, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - INDEX FOLLOW: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                try:
                    self.perform_test_steps(driver, text_to_find, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - NOINDEX FOLLOW: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, text_to_find, url):
        self.common_functions = TestCommonFunctions()
        time.sleep(5)
        print("PERFORM AARP PAGE META TAGS NOINDEX FOLLOW TEST STEPS START")
        # self.full_page_screenshot_lp = lambda x: driver.execute_script(
        #     'return document.body.parentNode.scroll' + x)
        # driver.set_window_size(self.full_page_screenshot_lp('Width'),
        #                             self.full_page_screenshot_lp('Height'))  # May need manual adjustment
        # # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot_' + url.split('/')[4] + '.png')
        if text_to_find in driver.page_source:
            print(text_to_find + " is present")
        else:
            print(text_to_find + " is not present")

            """ email sending if issues there in noindex follow """
            subject = "ALERT! Test Case Failed for noindex follow"
            body = text_to_find + " is not present in the URL " + url
            self.common_functions.send_email(subject, body)
        print("PERFORM AARP PAGE META TAGS NOINDEX FOLLOW  TEST STEPS END")
