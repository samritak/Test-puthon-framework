import time
import ssl, sys
import smtplib, pytest
from selenium.webdriver.common.by import By
from email.message import EmailMessage
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpHttpsLinkVerification:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - HTTPS LINK VERIFICATION")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        if base_url != "None":
            try:
                print("TESTING THE URL: " + base_url)
                driver = self.common_functions.open_browser(
                    base_url, Global_Env_Data.CHROME
                )
                time.sleep(20)
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - HTTPS LINK VERIFICATION: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(20)
                try:
                    self.perform_test_steps(driver, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - HTTPS LINK VERIFICATION: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("PERFORM AARP PAGE HREF LINKS TEST STEPS START")
        # self.full_page_screenshot_lp = lambda x: self.driver.execute_script(
        #     'return document.body.parentNode.scroll' + x)
        # self.driver.set_window_size(self.full_page_screenshot_lp('Width'),
        #                             self.full_page_screenshot_lp('Height'))  # May need manual adjustment
        # self.driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        # self.common_functions = TestCommonFunctions()

        all_links = driver.find_elements(By.TAG_NAME, "a")
        time.sleep(10)
        self.count = []
        for link in all_links:
            time.sleep(3)
            href = link.get_attribute("href")
            if href and (href.startswith("https://")):
                valid = True
                # print(f"Verified the https for all links present in the page")
            else:
                try:
                    if href.startswith("h"):
                        print(f" link : {href} is not valid")
                        self.count.append(href)
                except AttributeError as e:
                    non_http = True
        if len(self.count) != 0:
            self.send_mail(self.count, url)
        print("Verified the href for all the links present in the page.")
        print("PERFORM AARP PAGE HREF LINKS TEST STEPS ENDS")

    def send_mail(self, hrefs, url):
        self.common_functions = TestCommonFunctions()
        """ email sending if https not present in the URL"""
        self.urls = ""
        try:
            for i in hrefs:
                if i.startswith("h"):
                    self.urls = self.urls + str(i) + "\n"
        except AttributeError as e:
            non_http = True

        subject = "ALERT! Test Case Failed for href"
        body = (
            "Landing page" + " " + url + "\n"
            " Below urls which does not starts with https:" + "\n" + str(self.urls)
        )
        self.common_functions.send_email(subject, body)
