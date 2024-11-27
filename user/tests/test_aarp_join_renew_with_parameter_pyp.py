import time
from selenium.webdriver.common.by import By
import json, pytest, sys

from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpJoinRenewWithParameterPyp:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - JOIN PAGE WITH PARAMETER Hero")
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
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(
                    f"AN ERROR OCCURRED IN TEST - - JOIN PAGE WITH PARAMETERS Hero: {e}"
                )
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print(
                    "========================================================================\n"
                )
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(20)
                try:
                    self.perform_test_steps(driver, url)
                except Exception as e:
                    print(
                        f"AN ERROR OCCURRED IN TEST - JOIN PAGE WITH PARAMETERS Hero: {e}"
                    )
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        if "jkc1" in url:
            for i in range(1, 3):
                premium_select = "aarp-lp-js--dynPremium" + str(i)
                print("premium_select " + premium_select)
                try:
                    get_by_class_dyn = driver.find_element(
                        By.CLASS_NAME, premium_select
                    )
                except Exception as e:
                    print("Please check if page has PYP option")
                    return
                self.common_functions.button_click(driver, get_by_class_dyn)
                time.sleep(2)
                self.join_check(driver)
                time.sleep(5)
                self.renew_check(driver)
        else:
            time.sleep(2)
            self.join_check(driver)
            time.sleep(5)
            self.renew_check(driver)

    def join_check(self, driver):
        count = 0
        time.sleep(2)
        print("PERFORM JOIN PARAMETER Hero TEST STEPS START")
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)
        get_by_class_pyp = driver.find_element(By.CLASS_NAME, "aarp-lp-pyp--active")
        get_by_class_pyp_str = str(get_by_class_pyp.get_attribute("class")).split(" ")

        if "jkc" in json_lp_page:
            print("jkc jkc jkc")
            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["rkc"]
            json_lp_page_temp["campaignid"] = json_lp_page["jkc"]
            del json_lp_page_temp["jkc"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)
        elif "jkc1" in json_lp_page:
            print("jkc2 jkc1 jkc2")
            self.join_check_pyp(driver, get_by_class_pyp)

        self.common_functions.click_join_button(driver)
        time.sleep(2)
        self._application_page_url = self.common_functions.page_url(driver)
        self._qs_json_application_page = self.common_functions.qs_as_json_object(
            self._application_page_url
        )

        self.common_functions.compare_all_qs_params_in_json(
            self._path,
            self._application_page_url,
            self._qs_json_lp_page,
            self._qs_json_application_page,
            self._page_url,
            "join",
        )
        time.sleep(2)
        driver.back()
        time.sleep(5)
        if "jkc1" in json_lp_page:
            get_by_class_dyn = driver.find_element(
                By.CLASS_NAME, get_by_class_pyp_str[0]
            )
            self.common_functions.button_click(driver, get_by_class_dyn)

        get_by_class = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--joinNow")
        app_json_load = json.loads(self._qs_json_application_page)
        for i in get_by_class:
            i_href_json = self.common_functions.qs_as_json_object(
                i.get_attribute("href")
            )
            i_href_json = json.loads(i_href_json)
            if (
                str(app_json_load["campaignid"]).lower()
                == str(i_href_json["campaignid"]).lower()
            ):
                continue
            else:
                print("Join campaign  ID Not Matching --------------!!!\n\n")
                count = +1

        time.sleep(5)
        if count > 0:
            self.send_mail_cta(
                self,
                driver,
                "join button query string are not matching",
                self._page_url,
            )
            print("sent error email")
        else:
            print("PERFORM JOIN PARAMETER matching in all urls")

        print("PERFORM JOIN PARAMETER HERO TEST STEPS END")

    def join_check_pyp(self, driver, get_by_class_pyp):
        count = 0
        time.sleep(2)
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)
        self.common_functions.button_click(driver, get_by_class_pyp)
        time.sleep(2)
        active_pyp = get_by_class_pyp.get_attribute("class")
        if "aarp-lp-js--dynPremium1" in active_pyp:
            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["rkc1"]
            del json_lp_page_temp["rkc2"]
            del json_lp_page_temp["jkc2"]
            json_lp_page_temp["campaignid"] = json_lp_page["jkc1"]
            del json_lp_page_temp["jkc1"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)
        elif "aarp-lp-js--dynPremium2" in active_pyp:
            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["rkc1"]
            del json_lp_page_temp["rkc2"]
            del json_lp_page_temp["jkc1"]
            json_lp_page_temp["campaignid"] = json_lp_page["jkc2"]
            del json_lp_page_temp["jkc2"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)

    def renew_check(self, driver):
        count = 0
        time.sleep(2)
        print("PERFORM RENEW PARAMETER Hero TEST STEPS START")
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)
        get_by_class_pyp = driver.find_element(By.CLASS_NAME, "aarp-lp-pyp--active")
        get_by_class_pyp_str = str(get_by_class_pyp.get_attribute("class")).split(" ")

        if "jkc" in json_lp_page:
            print("jkc jkc jkc")

            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["jkc"]
            json_lp_page_temp["campaignid"] = json_lp_page["rkc"]
            del json_lp_page_temp["rkc"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)
        elif "jkc1" in json_lp_page:
            print("jkc2 jkc1 jkc2")
            self.renew_check_pyp(driver, get_by_class_pyp)

        self.common_functions.click_renew_button(driver)
        time.sleep(2)
        self._application_page_url = self.common_functions.page_url(driver)
        self._qs_json_application_page = self.common_functions.qs_as_json_object(
            self._application_page_url
        )

        self.common_functions.compare_all_qs_params_in_json(
            self._path,
            self._application_page_url,
            self._qs_json_lp_page,
            self._qs_json_application_page,
            self._page_url,
            "renew",
        )
        time.sleep(2)
        driver.back()
        time.sleep(5)
        if "jkc1" in json_lp_page:
            get_by_class_dyn = driver.find_element(
                By.CLASS_NAME, get_by_class_pyp_str[0]
            )
            self.common_functions.button_click(driver, get_by_class_dyn)

        get_by_class = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--renew")
        app_json_load = json.loads(self._qs_json_application_page)
        for i in get_by_class:
            i_href_json = self.common_functions.qs_as_json_object(
                i.get_attribute("href")
            )
            i_href_json = json.loads(i_href_json)
            if (
                str(app_json_load["campaignid"]).lower()
                == str(i_href_json["campaignid"]).lower()
            ):
                continue
            else:
                print("Renew campaign  ID Not Matching --------------!!!\n\n")
                count = +1

        time.sleep(5)
        if count > 0:
            self.send_mail_cta(
                self,
                driver,
                "RENEW button query string are not matching",
                self._page_url,
            )
            print("sent error email")
        else:
            print("PERFORM renew PARAMETER matching in all urls")

        print("PERFORM RENEW PARAMETER HERO TEST STEPS END")

    def renew_check_pyp(self, driver, get_by_class_pyp):
        count = 0
        time.sleep(2)
        self.common_functions = TestCommonFunctions()
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        json_lp_page = json.loads(self._qs_json_lp_page)
        self.common_functions.button_click(driver, get_by_class_pyp)
        time.sleep(2)
        active_pyp = get_by_class_pyp.get_attribute("class")
        # print(str(active_pyp))
        if "aarp-lp-js--dynPremium1" in active_pyp:
            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["jkc1"]
            del json_lp_page_temp["jkc2"]
            del json_lp_page_temp["rkc2"]
            json_lp_page_temp["campaignid"] = json_lp_page["rkc1"]
            del json_lp_page_temp["rkc1"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)
        elif "aarp-lp-js--dynPremium2" in active_pyp:
            json_lp_page_temp = json.loads(self._qs_json_lp_page)
            del json_lp_page_temp["jkc1"]
            del json_lp_page_temp["jkc2"]
            del json_lp_page_temp["rkc1"]
            json_lp_page_temp["campaignid"] = json_lp_page["rkc2"]
            del json_lp_page_temp["rkc2"]
            self._qs_json_lp_page = json.dumps(json_lp_page_temp)
            json_lp_page = json.loads(self._qs_json_lp_page)

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Cta Click Functionality"
        body = error_message + " URL: " + url
        common_functions.send_email(subject, body)
