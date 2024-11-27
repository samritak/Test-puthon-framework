import time, pytest, sys

from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpRenewPageWithParameter:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - RENEW PAGE WITH PARAMETER")
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
                self.perform_test_steps(driver)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - RENEW PAGE WITH PARAMETER: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(20)
                try:
                    self.perform_test_steps(driver)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - RENEW PAGE WITH PARAMETER: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver):
        print("PERFORM RENEW PARAMETER TEST STEPS START")
        self.common_functions = TestCommonFunctions()
        time.sleep(5)
        self.full_page_screenshot_lp = lambda x: driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        driver.set_window_size(
            self.full_page_screenshot_lp("Width"),
            self.full_page_screenshot_lp("Height"),
        )  # May need manual adjustment
        driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/onload_screenshot.png"
        )
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot_' + url.split('/')[4] + '.png')
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        time.sleep(5)
        self.common_functions.click_renew_button(driver)
        self._findme_page_url = self.common_functions.page_url(driver)
        time.sleep(6)
        self.full_page_screenshot_app = lambda x: driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        driver.set_window_size(
            self.full_page_screenshot_app("Width"),
            self.full_page_screenshot_app("Height"),
        )  # May need manual adjustment
        driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/application_page.png"
        )
        self._qs_json_findme_page = self.common_functions.qs_as_json_object(
            self._findme_page_url
        )
        self.common_functions.compare_all_qs_params_in_json(
            self._path,
            self._findme_page_url,
            self._qs_json_lp_page,
            self._qs_json_findme_page,
            self._page_url,
            "renew",
        )
        # self._tc_campaign = self.common_functions.qs_value_from_name(self._findme_page_url, 'tc_campaign')
        # self._tc_channel = self.common_functions.qs_value_from_name(self._findme_page_url, 'tc_channel')
        # self._tc_vendor = self.common_functions.qs_value_from_name(self._findme_page_url, 'tc_vendor')
        print("PERFORM RENEW PARAMETER TEST STEPS END")
