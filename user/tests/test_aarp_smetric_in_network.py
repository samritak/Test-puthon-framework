import time

from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions
from user.tests.semetric_network import *
import pytest, sys


class TestAarpSmetricInNetwork:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - SMETRICS NETWORK")
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
                print(f"AN ERROR OCCURRED IN TEST - SMETRICS NETWORK: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(20)
                try:
                    self.perform_test_steps(driver, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - SMETRICS NETWORK: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("\nPERFORM SMETRIC NETWORK TEST STEPS START")
        current_url = url
        self.parsed_url = urlparse(current_url)
        driver.refresh()
        time.sleep(10)
        driver.execute_cdp_cmd("Network.enable", {})
        # Capture network log entries
        log_entries = driver.get_log("performance")
        execute_network_logs = driver.execute_script(
            "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; "
            "var networkEntries = performance.getEntries() || []; "
            "var simplifiedEntries = networkEntries.map(function(entry){return {"
            " name: entry.name,entryType: entry.entryType,startTime: entry.startTime, duration: entry.duration,initiatorType: entry.initiatorType,"
            "nextHopProtocol: entry.nextHopProtocol};}); return simplifiedEntries;"
        )

        self.full_page_screenshot_lp = lambda x: driver.execute_script(
            "return document.body.parentNode.scroll" + x
        )
        driver.set_window_size(
            self.full_page_screenshot_lp("Width"),
            self.full_page_screenshot_lp("Height"),
        )  # May need manual adjustment
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        time.sleep(3)
        driver.find_element("tag name", "body").screenshot(
            "user/static/reports/html/screenshot/onload_screenshot_" + url.split("/")[4] + ".png"
        )
        time.sleep(3)
        SemetricNetwork.main_functionality(
            self, log_entries, driver, url, execute_network_logs, url
        )
        print("PERFORM SMETRIC NETWORK TEST STEPS END")
