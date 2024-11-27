import time

from user.tests.test_base_template import BaseTemplate
from user.tests.aarp_pyp_join_page_without_parameter import PypJoinPage
from user.Config.config import Global_Env_Data
import csv


class TestAarpPypJoinPageWithoutParameter(BaseTemplate):
    def test_join(self):
        self.contents = []
        path_to_file = (
            Global_Env_Data.LOCAL_PATH + Global_Env_Data.TEMPLATE_PYP_WITHOUT_PARAMETER
        )
        with open(path_to_file, mode="r") as file:
            cp_url = csv.reader(file)
            for row in cp_url:
                url = row[0]
                self.contents.append(url)

            for url in self.contents:
                print("Testing the below URL")
                print(url)
                self.join_page = PypJoinPage(self.driver, url)

                # Perform the test steps
                self.perform_test_steps_premium1()

                self.driver.execute_script("window.history.go(-1)")

                # Clear cookies and refresh the page
                self.driver.delete_all_cookies()
                print("Cookies cleared")
                self.driver.refresh()

                # Perform the test steps
                self.perform_test_steps_premium2()

                # Clear cookies and refresh the page
                self.driver.delete_all_cookies()
                print("Cookies cleared")
                self.driver.refresh()

                print("URL testing completed.")
                print("\n")

            print("********* END OF REPORT *********")
            print("\n")

            self.driver.quit()

    def perform_test_steps_premium1(self):
        self.full_page_screenshot_lp = lambda x: self.driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        self.driver.set_window_size(
            self.full_page_screenshot_lp("Width"),
            self.full_page_screenshot_lp("Height"),
        )  # May need manual adjustment
        self.driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/onload_screenshot.png"
        )

        self._page_url = self.join_page.page_url()

        self._host_name = self.join_page.host_name(self._page_url)

        self._path = self.join_page.path_name(self._page_url)

        self.join_page.query_string_present(self._page_url)

        self._default_premium = self.join_page.default_premium()

        self._default_jkc1 = self.join_page.default_campaignid("premium1", "jkc")
        self._default_jkc2 = self.join_page.default_campaignid("premium2", "jkc")

        print("Premium 1: \n")
        if self._default_premium == "premium2":
            # select premium 1
            print("select premium 1")
            self.join_page.select_premium("premium1")

        self.join_page.click_join_button()

        self._application_page_url = self.join_page.page_url()
        time.sleep(2)

        self.full_page_screenshot_app = lambda x: self.driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        self.driver.set_window_size(
            self.full_page_screenshot_app("Width"),
            self.full_page_screenshot_app("Height"),
        )  # May need manual adjustment
        self.driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/application_page.png"
        )

        self._campaign_id = self.join_page.qs_value_from_name(
            self._application_page_url, "campaignid"
        )

        self._tc_hpc = self.join_page.qs_value_from_name(
            self._application_page_url, "tc_hpc"
        )

        self._tc_tm_version = self.join_page.qs_value_from_name(
            self._application_page_url, "tc_tm_version"
        )

        self.join_page.compare_qs_values(
            "campaignid", self._default_jkc1, self._campaign_id
        )

        self.join_page.compare_qs_values("tc_hpc", self._host_name, self._tc_hpc)
        self.join_page.compare_qs_values(
            "tc_tm_version", self._path, self._tc_tm_version
        )

    def perform_test_steps_premium2(self):
        self.full_page_screenshot_lp = lambda x: self.driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        self.driver.set_window_size(
            self.full_page_screenshot_lp("Width"),
            self.full_page_screenshot_lp("Height"),
        )  # May need manual adjustment
        self.driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/onload_screenshot.png"
        )

        self._page_url = self.join_page.page_url()

        self._host_name = self.join_page.host_name(self._page_url)

        self._path = self.join_page.path_name(self._page_url)

        self.join_page.query_string_present(self._page_url)

        self._default_premium = self.join_page.default_premium()

        self._default_jkc1 = self.join_page.default_campaignid("premium1", "jkc")
        self._default_jkc2 = self.join_page.default_campaignid("premium2", "jkc")

        print("Premium 2: \n")
        if self._default_premium == "premium1":
            self.join_page.select_premium("premium2")

        self.join_page.click_join_button()

        self._application_page_url2 = self.join_page.page_url()
        time.sleep(2)

        self.full_page_screenshot_app = lambda x: self.driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        self.driver.set_window_size(
            self.full_page_screenshot_app("Width"),
            self.full_page_screenshot_app("Height"),
        )  # May need manual adjustment
        self.driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/application_page2.png"
        )

        self._campaign_id = self.join_page.qs_value_from_name(
            self._application_page_url2, "campaignid"
        )

        self._tc_hpc = self.join_page.qs_value_from_name(
            self._application_page_url2, "tc_hpc"
        )

        self._tc_tm_version = self.join_page.qs_value_from_name(
            self._application_page_url2, "tc_tm_version"
        )

        self.join_page.compare_qs_values(
            "campaignid", self._default_jkc2, self._campaign_id
        )

        self.join_page.compare_qs_values("tc_hpc", self._host_name, self._tc_hpc)
        self.join_page.compare_qs_values(
            "tc_tm_version", self._path, self._tc_tm_version
        )
