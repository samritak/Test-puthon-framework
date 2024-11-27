import time, sys, pytest
from selenium.webdriver.common.by import By
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpFaqPageCheck:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - FAQ Checklist begins")
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
                print(f"AN ERROR OCCURRED IN TEST - AARP FAQ PAGE CHECK: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print(
                    "========================================================================"
                )
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)

                time.sleep(5)
                try:
                    if "faq" in url:
                        self.perform_test_steps(driver, url)
                    else:
                        print("Please provide only FAQ pages for this test")
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - AARP FAQ PAGE CHECK: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("PERFORM AARP FAQ CHECK TEST STEPS START")
        error_count = 0
        try:
            try:
                link_exists1 = driver.find_elements(By.PARTIAL_LINK_TEXT, "8")
                if link_exists1:
                    for i in link_exists1:
                        href_link = i.get_attribute("href")
                        if (
                            href_link == "tel:1-888-687-2277"
                            or href_link == "tel:+1-888-687-2277"
                            or href_link == "tel:1-866-804-1278"
                            or href_link == "tel:+1-866-804-1278"
                            or href_link == "tel:1-866-684-9291"
                            or href_link == "tel:+1-866-684-9291"
                        ):
                            print("TFN href link is correct")
                        else:
                            error_count += 1
                            print("TFN href is not correct")
                else:
                    print("text link does not exist for this page " + url)
                    # time.sleep(6)
            except:
                print("exception, TFN link text does not exist")
            print("=============")
            title = driver.find_elements(By.TAG_NAME, "h1")
            if len(title) == 1:
                print("Only 1 h1 tag is present")
            else:
                error_count += 1
                print("more than 1 h1 tag or no h1 tag is present")
            print("=============")
            time.sleep(2)
            all_links = driver.find_elements(By.TAG_NAME, "a")
            if len(all_links) > 0:
                for link in all_links:
                    href = link.get_attribute("href")
                    if href is not None and (href.startswith("https://")):
                        continue
                    else:
                        if href is not None:
                            if href.startswith("http://"):
                                print(f" link : {href} is not valid")
                                error_count += 1
                print("all are https links")
            print("=============")
            can_links = driver.find_elements(By.TAG_NAME, "link")
            for ca_link in can_links:
                rel = ca_link.get_attribute("rel")
                if rel == "canonical":
                    # print("match 1")
                    if ca_link.get_attribute("href").endswith("/"):
                        if (
                            url.strip()
                            == "https://www.aarp.org/membership/faqs/can-i-gift-an-aarp-membership2/"
                        ):
                            print(
                                f" link : {ca_link.get_attribute('href')} is valid canonical tag"
                            )
                            continue
                        if ca_link.get_attribute("href").strip() == url.strip():
                            print(
                                f" link : {ca_link.get_attribute('href')} is valid canonical tag"
                            )
                        elif "2/" in url:
                            strip = url.rstrip("2/")
                            if ca_link.get_attribute("href").rstrip("/") == strip:
                                print(
                                    f" link : {ca_link.get_attribute('href')} is valid canonical tag"
                                )
                            else:
                                error_count += 1
                                print(
                                    f" link : {ca_link.get_attribute('href')} is invalid canonical tag"
                                )
                        else:
                            error_count += 1
                    else:
                        error_count += 1
            if error_count > 0:
                print("error count :" + str(error_count))
                self.send_mail_cta(self, driver, "FAQ criteria is not matched ", url)
        except Exception as e:
            # raise e from None
            print(e)
        print("PERFORM AARP FAQ CHECKIST TEST STEPS ENDS")

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Cta Click Functionality"
        body = error_message + " URL: " + url
        common_functions.send_email(subject, body)
