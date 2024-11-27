from pathlib import Path
from user.tests.test_base_template import BaseTemplate
from user.tests.aarp_join_page_without_parameter import JoinPage
from selenium.webdriver.common.by import By
from user.Config.config import Global_Env_Data
import csv, time, os, pytest, sys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox, FirefoxOptions
from selenium import webdriver


class TestAarpScrollupScrolldownZoominZoomout(BaseTemplate):
    @pytest.mark.nondestructive
    def test_join(self):
        self.driver.quit()
        self.contents = []
        # path_to_file = Global_Env_Data.LOCAL_PATH + Global_Env_Data.TEMPLATE_DIFFERENT_BROWSER_WIDTHS_PARAMETER
        # path_to_file = str(Path(os.getcwd()).parent.absolute()) + Global_Env_Data.multiURls
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
                print(f"AN ERROR OCCURRED IN TEST - AARP PAGE META TAGS: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            path_to_file = os.getcwd() + Global_Env_Data.MULTI_URLS
            with open(path_to_file, mode="r") as file:
                cp_url = csv.reader(file)
                for row in cp_url:
                    url = row[0]
                    self.contents.append(url)

                for url in self.contents:
                    print("Testing the below URL")
                    print(url)
                    self.driver = webdriver.Firefox()
                    self.driver.get(url)

                    # Perform the test steps
                    self.perform_test_steps(self.driver, url)

                    # Clear cookies and refresh the page
                    self.driver.delete_all_cookies()
                    print("Cookies cleared")
                    self.driver.refresh()

                    print("URL testing completed.")
                    print("\n")

                print("********* END OF REPORT *********")
                print("\n")

                self.driver.quit()

    def perform_test_steps(self, driver, url):
        opts: Options = FirefoxOptions()
        width = [375, 768, 1440, 2000]
        scroll_height = 450
        for index in width:
            time.sleep(15)
            # driver = webdriver.Firefox()
            self.join_page = JoinPage(self.driver, url)
            print("Screen width: ")
            print(index)
            driver.delete_all_cookies()
            time.sleep(3)
            driver.set_window_size(index, height=800)
            driver.get(url)
            time.sleep(3)
            script = f"window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(script)
            time.sleep(3)
            script = f"window.scrollTo(0, 0);"
            driver.execute_script(script)
            time.sleep(3)
        """ we have made zoomin and zoomout made inactive """
        #     zoom_percentages = [50, 67, 90, 100, 110, 120, 133, 150, 170, 200, 240]
        # for zoom_size in zoom_percentages:
        #     val = "//*[@value='" + str(zoom_size) + "']"
        #     print(val)
        #     driver.get("about:preferences")
        #     driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//*[@id='defaultZoom']"))
        #     ActionChains(driver).click(driver.find_element(By.XPATH, val)).perform()
        #     self.join_page = JoinPage(driver, url)
        #     script = f"window.scrollTo(0, document.body.scrollHeight);"
        #     driver.execute_script(script)
        #     time.sleep(3)
        #     script = f"window.scrollTo(0, 0);"
        #     driver.execute_script(script)
        #     time.sleep(3)
