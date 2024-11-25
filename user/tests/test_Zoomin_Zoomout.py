from test_Template import BaseTemplate
from JoinPage_WithoutParameter import JoinPage
from selenium.webdriver.common.by import By
import csv, time,os, sys, pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox, FirefoxOptions
from Config.config import Global_Env_Data
from CommonFunctions import TestCommonFunctions
class TestScrollup_Scrolldown_Zoomin_Zoomout(BaseTemplate):

    @pytest.mark.nondestructive
    def test_run_test_case(self):

        print("TEST CASE BEGIN - AARP ZOOMIN AND ZOOMOUT")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != 'None':
            try:
                print("TESTING THE URL: " + base_url)
                driver = self.common_functions.open_browser(base_url, Global_Env_Data.CHROME)
                time.sleep(20)
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - AARP PAGE META TAGS: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(5)
                try:
                    self.perform_test_steps(self.driver, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - AARP PAGE META TAGS: {e}")
                finally:
                    self.common_functions.close_browser(driver)
    # def test_join(self):
    #     self.driver.quit()
    #     self.contents = []
    #     # path_to_file = Global_Env_Data.LOCAL_PATH + Global_Env_Data.TEMPLATE_DIFFERENT_BROWSER_WIDTHS_PARAMETER
    #     path_to_file = os.getcwd() + Global_Env_Data.multiURls
    #     with open(path_to_file, mode='r') as file:
    #         cp_url = csv.reader(file)
    #         for row in cp_url:
    #             url = row[0]
    #             self.contents.append(url)
    #
    #         for url in self.contents:
    #             print("Testing the below URL")
    #             print(url)
    #             self.driver = webdriver.Firefox()
    #             self.driver.get(url)
    #             self.join_page = JoinPage(self.driver, url)
    #
    #             # Perform the test steps
    #             self.perform_test_steps(self.driver, url)
    #
    #             # Clear cookies and refresh the page
    #             self.driver.delete_all_cookies()
    #             print("Cookies cleared")
    #             self.driver.refresh()
    #
    #             print("URL testing completed.")
    #             print("\n")
    #
    #         print("********* END OF REPORT *********")
    #         print("\n")
    #
    #         self.driver.quit()

    def perform_test_steps(self, driver, url):
        print("PERFORM AARP PAGE ZOOMIN AND ZOOMOUT START")
        #self.join_page = JoinPage(driver, url)
        #driver.maximize_window()
        # driver.find_element(By.TAG_NAME,'body').send_keys(Keys.CONTROL + '+')
        zoom_percentages = [50, 90, 100, 120, 150, 170, 200, 240]
        for zoom_size in zoom_percentages:
            time.sleep(10)
            val = "//*[@value='" + str(zoom_size) + "']"
            print(val)
            driver.get("about:preferences")
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//*[@id='defaultZoom']"))
            ActionChains(driver).click(driver.find_element(By.XPATH, val)).perform()
            self.join_page = JoinPage(driver, url)
            time.sleep(10)
            self.driver.find_element("tag name", "body").screenshot(
                'Reports/html/screenshot/zoom_img_' + str(zoom_size) + '.png')
        print("PERFORM AARP PAGE ZOOMIN AND ZOOMOUT ENDS")
            # time.sleep(6)
        # driver.quit()
