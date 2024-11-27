import time
from selenium.webdriver.common.by import By
import json
import pytest, sys
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpCategoryLevelAccord:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - Category Level Accord")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        if base_url != "None":
            print("TESTING THE URL: " + base_url)
            driver = self.common_functions.open_browser(
                base_url, Global_Env_Data.CHROME
            )
            time.sleep(5)
            try:
                if "category" in base_url:
                    accordian_exists = driver.find_elements(
                        By.CLASS_NAME, "cmp-experiencefragment--accordion"
                    )
                    if accordian_exists:
                        if "memday" in base_url or "flashsale" in base_url:
                            if "btf=a" in base_url:
                                self.perform_test_steps(driver, base_url)
                            else:
                                print(
                                    "Accordian does not exist for this page " + base_url
                                )
                        else:
                            self.perform_test_steps(driver, base_url)
                    else:
                        print("Accordian does not exist for this page " + base_url)
                else:
                    print("url does not have category")

            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - Category Level Accord: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print(
                    "========================================================================\n"
                )
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(5)
                try:
                    if "category" in url:
                        accordian_exists = driver.find_elements(
                            By.CLASS_NAME, "cmp-experiencefragment--accordion"
                        )
                        if accordian_exists:
                            if "memday" in url or "flashsale" in url:
                                if "btf=a" in url:
                                    self.perform_test_steps(driver, url)
                                else:
                                    print(
                                        "Accordian does not exist for this page " + url
                                    )
                            else:
                                self.perform_test_steps(driver, url)
                        else:
                            print("Accordian does not exist for this page " + url)
                    else:
                        print("url does not have category")

                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - Category Level Accord: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("inside perform_test_steps of Category Level Accord")
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)

        flag = 0
        get_by_class_accord = driver.find_elements(
            By.CLASS_NAME, "aarp-c-accordion-lp__accTab"
        )
        if json_lp_page:
            for i in get_by_class_accord:
                # print(i.get_attribute('title'))
                if str(json_lp_page["category"][0]).split("_")[0] == "technology":
                    category_qs = "tech"
                elif str(json_lp_page["category"][0]).split("_")[0] == "restaurants":
                    category_qs = "food"
                elif str(json_lp_page["category"][0]).split("_")[0] == "car":
                    category_qs = "auto"
                else:
                    category_qs = str(json_lp_page["category"][0]).split("_")[0]
                if category_qs in str(i.get_attribute("title")).lower().split(" "):
                    flag = 1
                    # print(str(i.get_attribute('title')).lower().split(" "))
                    if "order: -2;" in i.get_attribute("style"):
                        print(
                            str(json_lp_page["category"][0])
                            + " is set first in the accordian"
                        )
                        get_by_class_accord_body = driver.find_elements(
                            By.CLASS_NAME, "aarp-js-accordion-lp__panel"
                        )
                        concat_str = "aarp-js-accordion-lp__panel" + str(
                            i.get_attribute("rel")
                        )

                        for x in get_by_class_accord_body:
                            if str(x.get_attribute("id")) == concat_str:
                                if (
                                    str(x.get_attribute("style"))
                                    == "display: block; order: -1;"
                                ):
                                    print("Correct accordian is open!")
                                else:
                                    print("accordian closed!")
                                    self.send_mail_cta(
                                        self,
                                        driver,
                                        "category is first but accordian is not open",
                                        self._page_url,
                                    )
                                    print("sent error email")
                else:
                    continue
            if flag == 0:
                print("pLease check the category value in URL")
        else:
            print("Query string value is empty")

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Category Level Accord"
        body = error_message + " URL: " + url
        common_functions.send_email(subject, body)
