import time,pytest,sys
from selenium.webdriver.common.by import By
from user.Config.config import Global_Env_Data
from CommonFunctions import TestCommonFunctions

class TestLgCopyTextVerification:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - TestCopyTextVerification")
        self.common_functions = TestCommonFunctions()
        self.csv_contents = self.common_functions.get_template_csv_file()
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != 'None':
                print("TESTING THE URL: " + base_url)
                time.sleep(10)
                self.perform_test_steps(base_url)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                self.perform_test_steps(url)

    def perform_test_steps(self, url):
            print("PERFORM AARP PAGE LG MEM COPY TEXT VERIFICATION TEST STEPS START")
            self.common_functions = TestCommonFunctions()
            width = [375, 1200]
            for index in width:
                time.sleep(5)
                print("SCREEN WIDTH: ", index)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(20)
                try:
                    driver.delete_all_cookies()
                    driver.set_window_size(index, height=800)
                    time.sleep(5)
                    if driver.find_elements(By.XPATH, "//div[contains(@class,'cmp-experiencefragment--header_leadgen')]"):
                        print("LeadGen nav bar is present in the landing page " + url)
                        self.common_functions.phone_number_verification(driver, url, Global_Env_Data.LG_COPY_TEXT_VERIFICATION)
                    elif driver.find_elements(By.XPATH, "//div[contains(@class,'cmp-experiencefragment--Header_Experience_Fragment')]"):
                        print("Membership nav bar is present in the landing page " + url)
                        self.common_functions.phone_number_verification(driver, url,Global_Env_Data.MEM_COPY_TEXT_VERIFICATION)
                    else:
                        print("LeadGen and Membership nav bar is not present in the landing page " + url)
                        """ email sending  """
                        subject = 'ALERT! Test Case Failed for LG nav bar'
                        body = " LeadGen and Membership nav bar is not present in the landing page " + url
                        self.common_functions.send_email(subject, body)
                        time.sleep(3)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - LG MEM COPY TEXT VERIFICATION: {e}")
                finally:
                    self.common_functions.close_browser(driver)
            print("PERFORM AARP PAGE LG MEM COPY TEXT VERIFICATION TEST STEPS END")
   