import time

from test_base_template import BaseTemplate
from user.tests.aarp_join_page_without_parameter import JoinPage
from user.Config.config import Global_Env_Data
import csv


class TestJoinPageWithoutParameter(BaseTemplate):
    def test_join(self):
        self.contents = []
        path_to_file = (
            Global_Env_Data.LOCAL_PATH + Global_Env_Data.TEMPLATE_WITHOUT_PARAMETER
        )
        with open(path_to_file, mode="r") as file:
            cp_url = csv.reader(file)
            for row in cp_url:
                url = row[0]
                self.contents.append(url)

            for url in self.contents:
                print("Testing the below URL")
                print(url)
                self.join_page = JoinPage(self.driver, url)

                # Perform the test steps
                self.perform_test_steps()

                # Clear cookies and refresh the page
                self.driver.delete_all_cookies()
                print("Cookies cleared")
                self.driver.refresh()

                print("URL testing completed.")
                print("\n")

            print("********* END OF REPORT *********")
            print("\n")

            self.driver.quit()

    def perform_test_steps(self):
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

        self.join_page.click_join_button()
        time.sleep(2)

        self._application_page_url = self.join_page.page_url()
        time.sleep(5)

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

        self.exp_name_match = self.join_page.search_name(self._path)

        # self.join_page.back_page()

        if self.exp_name_match == "sem":
            self.join_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_SEM_JOIN_CAMPAIGN_ID,
                self._campaign_id,
            )
        elif self.exp_name_match == "soc":
            self.join_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_SOC_JOIN_CAMPAIGN_ID,
                self._campaign_id,
            )
        elif self.exp_name_match == "dis":
            self.join_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_DIS_JOIN_CAMPAIGN_ID,
                self._campaign_id,
            )
        else:
            self.join_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_JOIN_CAMPAIGN_ID,
                self._campaign_id,
            )

        # self.join_page.compare_qs_values("tc_hpc", self._host_name, self._tc_hpc)
        # self.join_page.compare_qs_values("tc_tm_version", self._path, self._tc_tm_version)
