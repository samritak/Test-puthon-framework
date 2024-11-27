import ssl, time, pytest, sys
import smtplib
from email.message import EmailMessage
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestAarpVerifyCorrectPremiumName:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - AARP CORRECT PREMIUM NAME")
        verify_premium_name = Global_Env_Data.INCORRECT_PREMIUM_NAME
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
                time.sleep(20)
                self.perform_test_steps(verify_premium_name, driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - HTTPS LINK VERIFICATION: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(5)

                self.perform_test_steps(verify_premium_name, driver, url)
                self.common_functions.close_browser(driver)

    def perform_test_steps(self, verify_premium_name, driver, url):
        self.common_functions = TestCommonFunctions()
        print("PERFORM CORRECT PREMIUM NAME TEST STEPS START")
        self.full_page_screenshot_lp = lambda x: driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        driver.set_window_size(
            self.full_page_screenshot_lp("Width"),
            self.full_page_screenshot_lp("Height"),
        )  # May need manual adjustment
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/onload_screenshot_" + url.split("/")[4] + ".png"
        )
        classes = [
            "aarp-js-singleprem-lp__premium-name",
            "aarp-lp-js--dynTitle1",
            "aarp-lp-js--dynTitle2",
            "aarp-js-premium-lp--gift-name1",
            "aarp-js-premium-lp--gift-name2",
            "aarp-js-premium-lp--gift-name3",
            "aarp-js-premium-lp--gift-name4",
        ]
        premiumTitleList = []
        for item in classes:
            try:
                _element_present = WebDriverWait(driver, 3).until(
                    ec.visibility_of_element_located((By.CLASS_NAME, item))
                )
                if bool(_element_present) == True:
                    premiumTitleList.append(_element_present.get_attribute("innerText"))
            except:
                timeout = True
        if len(premiumTitleList) == 0:
            print("Premium name is not available in the page for the given campaignid")
        else:
            for premiumName in premiumTitleList:
                if len(premiumName) != 0:
                    if verify_premium_name in premiumName:
                        print(
                            "Incorrect premium name is displayed which contains special characters",
                            premiumName,
                        )
                        """ email sending  """
                        subject = "ALERT! Test Case Failed for premium name"
                        body = (
                            premiumName
                            + " - Incorrect premium name is displayed which contains special characters from the landing page URL "
                            + url
                        )
                        self.common_functions.send_email(subject, body)
                    else:
                        print("Valid premium name is present:", premiumName)
                else:
                    print("Premium is not available for the given campaignid")
                pass
            print("PERFORM CORRECT PREMIUM NAME TEST STEPS ENDS")
