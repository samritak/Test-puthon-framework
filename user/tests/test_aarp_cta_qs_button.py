import time
from selenium.webdriver.common.by import By
import json
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions
import pytest, sys


class TestAarpCtaQsButton:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - Test CTA Query String")
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
                print(f"AN ERROR OCCURRED IN TEST - Test CTA Query String: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print(
                    "========================================================================"
                )
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                try:
                    if "cta" in url:
                        self.perform_test_steps(driver, url)
                    else:
                        print("url does not have cta query string")

                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - Test CTA Query String: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        time.sleep(2)
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)

        get_by_join_class_accord = driver.find_elements(
            By.CLASS_NAME, "aarp-js-lp--joinNow"
        )
        get_by_renew_class_accord = driver.find_elements(
            By.CLASS_NAME, "aarp-js-lp--renew"
        )
        get_by_rejoin_class_accord = driver.find_elements(
            By.CLASS_NAME, "aarp-js-lp--rejoinNow"
        )
        join_count = 0
        renew_count = 0
        rejoin_count = 0
        if json_lp_page:
            if json_lp_page["cta"][0] == "j":
                for i in get_by_join_class_accord:
                    dataformelementid = i.get_attribute("data-formelementid")
                    parent_div = i.find_element(By.XPATH, "..")
                    if (
                        parent_div.tag_name == "div"
                        and parent_div.value_of_css_property("display") != "none"
                    ):
                        if (
                            "join"
                            in str(i.get_attribute("Title")).split(" ")[0].lower()
                        ):
                            continue
                        else:
                            self.send_mail_cta(
                                self,
                                driver,
                                "Wrong button Title in CTA",
                                self._page_url,
                            )
                            print(
                                str(i.get_attribute("Title"))
                                + "is the title, email sent!"
                            )
                    else:
                        div_link = parent_div.find_element(By.XPATH, "..")
                        if (
                            div_link.value_of_css_property("display") != "none"
                            and str(dataformelementid).lower() != "none"
                        ):
                            join_count += 1
                if join_count > 0:
                    self.send_mail_cta(
                        self,
                        driver,
                        "Join Button does not exist or hidden",
                        self._page_url,
                    )
                    print("Join Button does not exist or hidden, email sent!")
                else:
                    print("Join buttons are displayed correctly")

            elif json_lp_page["cta"][0] == "r":
                for i in get_by_renew_class_accord:
                    # dataformelementid = i.get_attribute('data-formelementid')
                    parent_div = i.find_element(By.XPATH, "..")
                    if (
                        parent_div.tag_name == "div"
                        and parent_div.value_of_css_property("display") != "none"
                    ):
                        if (
                            "renew"
                            in str(i.get_attribute("Title")).split(" ")[0].lower()
                        ):
                            # print("Renew Button is present")
                            continue
                        else:
                            # print("first else")
                            self.send_mail_cta(
                                self,
                                driver,
                                "Wrong button Title in CTA",
                                self._page_url,
                            )
                            print(
                                str(i.get_attribute("Title"))
                                + "is the title, email sent!"
                            )
                    else:
                        div_link = parent_div.find_element(By.XPATH, "..")
                        if (
                            div_link.value_of_css_property("display") != "none"
                        ):  # and str(dataformelementid).lower() != 'none':
                            renew_count += 1
                if renew_count > 0:
                    self.send_mail_cta(
                        self,
                        driver,
                        "Renew Button does not exist or hidden",
                        self._page_url,
                    )
                    print("Renew Button does not exist or hidden, email sent!")
                else:
                    print("Renew buttons are displayed correctly")

            elif json_lp_page["cta"][0] == "rejoin" or json_lp_page["cta"][0] == "w":
                for i in get_by_rejoin_class_accord:
                    parent_div = i.find_element(By.XPATH, "..")
                    # dataformelementid = i.get_attribute('data-formelementid')
                    if (
                        parent_div.tag_name == "div"
                        and parent_div.value_of_css_property("display") != "none"
                    ):
                        if (
                            "rejoin"
                            in str(i.get_attribute("Title")).split(" ")[0].lower()
                        ):
                            # print("Rejoin Button is present")
                            continue
                        else:
                            self.send_mail_cta(
                                self,
                                driver,
                                "Wrong button Title in CTA",
                                self._page_url,
                            )
                            print(
                                str(i.get_attribute("Title"))
                                + "is the title, email sent!!!"
                            )
                    else:
                        div_link = parent_div.find_element(By.XPATH, "..")
                        if (
                            div_link.value_of_css_property("display") != "none"
                        ):  # and str(dataformelementid).lower() != 'none' :
                            rejoin_count += 1
                if rejoin_count > 0:
                    self.send_mail_cta(
                        self,
                        driver,
                        "Rejoin Button does not exist or hidden",
                        self._page_url,
                    )
                    print("Rejoin Button does not exist or hidden, email sent!!!!")
                else:
                    print("Rejoin buttons are displayed correctly")
            else:
                print("please provide valid input for cta")
        else:
            print("cta value is empty")

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Cta Query string Functionality"
        body = error_message + " URL: " + url
        common_functions.send_email(subject, body)
