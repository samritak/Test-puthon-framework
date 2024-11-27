import time, pytest, sys

from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpJoinPageWithParameter:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - JOIN PAGE WITH PARAMETER")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        driver = None
        if base_url != "None":
            print("TESTING THE URL: " + base_url)
            try:
                driver = self.common_functions.open_browser(
                    base_url, Global_Env_Data.CHROME
                )
                time.sleep(20)
                self.perform_test_steps(driver)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - JOIN PAGE WITH PARAMETERS: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                try:
                    driver = self.common_functions.open_browser(
                        url, Global_Env_Data.CHROME
                    )
                    time.sleep(20)
                    self.perform_test_steps(driver)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - JOIN PAGE WITH PARAMETERS: {e}")
                finally:
                    if driver:
                        self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver):
        print("PERFORM JOIN PARAMETER TEST STEPS START")
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
        self._page_url = self.common_functions.page_url(driver)
        self._host_name = self.common_functions.host_name(self._page_url)
        self._path = self.common_functions.path_name(self._page_url)
        self._qs_json_lp_page = self.common_functions.qs_as_json_object(self._page_url)
        time.sleep(5)
        self.common_functions.click_join_button(driver)
        time.sleep(2)
        self._application_page_url = self.common_functions.page_url(driver)
        time.sleep(5)
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
        # self._tc_campaign = self.common_functions.qs_value_from_name(self._application_page_url, 'tc_campaign')
        # self._tc_channel = self.common_functions.qs_value_from_name(self._application_page_url, 'tc_channel')
        # self._tc_vendor = self.common_functions.qs_value_from_name(self._application_page_url, 'tc_vendor')
        print("PERFORM JOIN PARAMETER TEST STEPS END")
