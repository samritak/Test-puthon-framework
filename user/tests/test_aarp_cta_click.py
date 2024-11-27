import smtplib
import ssl
import time, pytest, sys
from email.message import EmailMessage

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions


class TestAarpCtaClick:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - TEST CTA CLICK FUNCTIONALITY")
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
                print(f"AN ERROR OCCURRED IN TEST - TEST CLICK: {e}")
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
                    print(f"AN ERROR OCCURRED IN TEST - TEST CLICK: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def perform_test_steps(self, driver, url):
        print("PERFORM AARP CLICK CTA TEST STEPS START")
        width = [375, 768, 1200, 1440]
        scroll_height = 450
        for index in width:
            driver.get(url)
            time.sleep(20)
            driver.set_window_size(index, height=800)
            time.sleep(6)
            # Clear cookies and refresh the page
            driver.delete_all_cookies()
            print("Cookies cleared")
            driver.refresh()
            print("Started testing on screen width: " + str(index))
            # print(index)
            scroll_height = 0
            for i in range(10):
                # print("range i ", i)
                script = f"window.scrollTo(0, {scroll_height});"
                # print(script)
                driver.execute_script(script)
                scroll_height += 800
                # print(scroll_height)
                time.sleep(4)
            # script = f"window.scrollTo(0, document.body.scrollHeight);"
            # driver.execute_script(script)
            time.sleep(5)
            script = f"window.scrollTo(0, 0);"
            driver.execute_script(script)
            time.sleep(5)
            # screen shot code starts\
            driver.find_element("tag name", "body").screenshot(
                "user/static/reports/html/screenshot/zoom_img_"
                + str(index)
                + "_"
                + url.split("/")[4]
                + ".png"
            )
            # screen shot code ends\
            self.click_join_now_cta(self, driver)
            time.sleep(3)
            self.click_renew_now_cta(self, driver)
            time.sleep(5)
            driver.maximize_window()
            time.sleep(5)
            driver.refresh()
            print("PERFORM AARP CLICK CTA TEST STEPS ENDS")

            # zoom code starts\
        #     zoom_percentages = [50]
        # for zoom_size in zoom_percentages:
        #     val = "//*[@value='" + str(zoom_size) + "']"
        #     print(val)
        #     driver.get("about:preferences")
        #     driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH, "//*[@id='defaultZoom']"))
        #     ActionChains(driver).click(driver.find_element(By.XPATH, val)).perform()
        #     driver.back()
        #     driver.refresh()
        #     time.sleep(8)
        #     self.join_now()
        #     self.renew_now()
        #     for i in range(5):
        #         print("range i ", i)
        #         script = f"window.scrollTo(0, {scroll_height});"
        #         print(script)
        #         driver.execute_script(script)
        #         scroll_height += 800
        #         print(scroll_height)
        #         time.sleep(8)
        #     # script = f"window.scrollTo(0, document.body.scrollHeight);"
        #     # driver.execute_script(script)
        #     time.sleep(8)
        #     script = f"window.scrollTo(0, 0);"
        #     driver.execute_script(script)
        #     time.sleep(8)
        #     driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/zoom_img_' + str(zoom_size) + '.png')
        #     driver.maximize_window()
        # zoom code ends\

    @staticmethod
    def click_join_now_cta(self, driver):
        print("JOIN CTA CLICK START")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        get_by_class = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--joinNow")
        time.sleep(3)
        first_url_link = get_by_class[0].get_attribute("href")
        # Click the first join button
        get_by_class[0].click()
        # Get the url of the active view page
        link_after_click = driver.current_url
        # Get the exact link and trim the extra query param added on naivation
        final_after_link = link_after_click.split("&")[0]
        time.sleep(5)
        driver.back()
        driver.refresh()
        time.sleep(5)
        if first_url_link.split("?")[0] == final_after_link.split("?")[0]:
            print("ALL JOIN CTA LINKS ARE MATCHING")
        get_by_class_new = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--joinNow")
        for links_value in get_by_class_new:
            time.sleep(3)
            get_urls = links_value.get_attribute("href")
            if get_urls.split("?")[0] != final_after_link.split("?")[0]:
                print("the url is not matching : ", get_urls)
                self.send_mail_cta(
                    self, driver, "Join Button CTA is not matching", get_urls
                )
                elements_not_clickable = driver.find_elements(
                    By.CSS_SELECTOR, ".aarp-js-lp--joinNow[style*='pointer-events']"
                )
                for element_not_clickable in elements_not_clickable:
                    if element_not_clickable:
                        not_clickable_link = element_not_clickable.get_attribute("href")
                        print("Join Button CTA is not clickable", not_clickable_link)
                        self.send_mail_cta(
                            self,
                            driver,
                            "Join Button CTA is not clickable",
                            not_clickable_link,
                        )
        print("JOIN CTA CLICK END")

    @staticmethod
    def click_renew_now_cta(self, driver):
        print("RENEW CTA CLICK START")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        get_by_class = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--renew")
        time.sleep(3)
        print("\n")
        first_url_link = get_by_class[0].get_attribute("href")
        # Click the first join button
        get_by_class[0].click()
        # Get the url of the active view page
        link_after_click = driver.current_url
        # Get the exact link and trim the extra query param added on navigation
        final_after_link = link_after_click.split("&")[0]
        time.sleep(4)
        driver.back()
        driver.refresh()
        time.sleep(5)
        if first_url_link.split("?")[0] == final_after_link.split("?")[0]:
            print("ALL RENEW CTA LINKS ARE MATCHING")
        get_by_class_new = driver.find_elements(By.CLASS_NAME, "aarp-js-lp--renew")
        for links_value in get_by_class_new:
            time.sleep(3)
            get_urls = links_value.get_attribute("href")
            if get_urls.split("?")[0] != final_after_link.split("?")[0]:
                print("the url is not matching : ", get_urls)
                self.send_mail_cta(
                    self, driver, "Renew Button CTA is not matching", get_urls
                )
                elements_not_clickable = driver.find_elements(
                    By.CSS_SELECTOR, ".aarp-js-lp--renew[style*='pointer-events']"
                )
                for element_not_clickable in elements_not_clickable:
                    if element_not_clickable:
                        not_clickable_link = element_not_clickable.get_attribute("href")
                        print("Renew Button CTA is not clickable", not_clickable_link)
                        self.send_mail_cta(
                            self,
                            driver,
                            "Renew Button CTA is not clickable",
                            not_clickable_link,
                        )
        print("RENEW CTA CLICK END")

    @staticmethod
    def send_mail_cta(self, driver, error_message, url):
        common_functions = TestCommonFunctions()
        subject = "ALERT! Test Case Failed for Cta Click Functionality"
        body = error_message + " URL: " + url
        common_functions.send_email(subject, body)
