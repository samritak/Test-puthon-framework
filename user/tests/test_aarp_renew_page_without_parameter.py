import time

from user.tests.test_base_template import BaseTemplate
from user.tests.aarp_renew_page_without_parameter import RenewPage
from user.Config.config import Global_Env_Data
import csv


class TestAarpRenewPageWithoutParameter(BaseTemplate):
    def test_renew(self):
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
                self.renew_page = RenewPage(self.driver, url)

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

        self._page_url = self.renew_page.page_url()

        self._host_name = self.renew_page.host_name(self._page_url)

        self._path = self.renew_page.path_name(self._page_url)

        self.renew_page.query_string_present(self._page_url)

        self.renew_page.click_renew_button()

        self._findme_page_url = self.renew_page.page_url()
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

        self._campaign_id = self.renew_page.qs_value_from_name(
            self._findme_page_url, "campaignid"
        )

        self._tc_hpc = self.renew_page.qs_value_from_name(
            self._findme_page_url, "tc_hpc"
        )

        self._tc_tm_version = self.renew_page.qs_value_from_name(
            self._findme_page_url, "tc_tm_version"
        )

        self.exp_name_match = self.renew_page.search_name(self._path)

        if self.exp_name_match == "sem":
            self.renew_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_SEM_RENEW_CAMPAIGN_ID,
                self._campaign_id,
            )
        elif self.exp_name_match == "soc":
            self.renew_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_SOC_RENEW_CAMPAIGN_ID,
                self._campaign_id,
            )
        elif self.exp_name_match == "dis":
            self.renew_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_DIS_RENEW_CAMPAIGN_ID,
                self._campaign_id,
            )
        else:
            self.renew_page.compare_qs_values(
                "campaignid",
                Global_Env_Data.DEFAULT_RENEW_CAMPAIGN_ID,
                self._campaign_id,
            )

        # self.renew_page.compare_qs_values("tc_hpc", self._host_name, self._tc_hpc)
        # self.renew_page.compare_qs_values("tc_tm_version", self._path, self._tc_tm_version)
