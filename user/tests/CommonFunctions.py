import csv
import os
import json
import re
import ssl
import smtplib
import json
import platform
import time
import cv2
from selenium.webdriver.chrome.options import Options as chrome_opts
from selenium.webdriver.firefox.options import Options as firefox_opts
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import numpy as np
from pathlib import Path
from user.Config.config import Global_Env_Data
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from email.message import EmailMessage
from email.utils import formataddr
import glob
import img2pdf
from PIL import Image
from selenium.webdriver import Firefox, FirefoxOptions


class TestCommonFunctions:
    Button_Click_Header_Join = (By.XPATH, '//*[@id="head_jn"]')
    Button_Click_Header_Renew = (By.XPATH, '//*[@id="head_rnw"]')

    @staticmethod
    def page_url(driver):
        return driver.current_url

    @staticmethod
    def host_name(url):
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        return hostname

    @staticmethod
    def path_name(url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        path_name = path.replace("/", "")
        return path_name

    def is_visible(self, driver, by_locator):
        element_present = WebDriverWait(driver, 20).until(ec.visibility_of_element_located(by_locator))
        return bool(element_present)

    def button_click(self, driver, by_locator):
        clicked = WebDriverWait(driver, 20).until(ec.element_to_be_clickable(by_locator))
        clicked.click()
        return bool(clicked)

    @staticmethod
    def get_sub_string_from_experience(experience_name):
        if re.search("^sem-", experience_name) or re.search("-sem-", experience_name) or re.search("-sem$",
                                                                                                   experience_name):
            return "sem"
        elif re.search("^soc-", experience_name) or re.search("-soc-", experience_name) or re.search("-soc$",
                                                                                                     experience_name):
            return "soc"
        elif re.search("^dis-", experience_name) or re.search("-dis-", experience_name) or re.search("-dis$",
                                                                                                     experience_name):
            return "dis"
        else:
            return "default"

    def compare_values(self, key, expected_value, passed_value):
        if expected_value == passed_value:
            line = "key: " + key + "\n" + "expected value: " + expected_value + "\n" + "passed value: " + passed_value + "\n" + "Result: Matched" + "\n"
            print(line)
        else:
            line = "key: " + key + "\n" + "expected value: " + expected_value + "\n" + "passed value: " + passed_value + "\n" + "Result: Not matched (X)" + "\n"
            print(line)

    def compare_query_string_parameters(self, page, experience_name, application_url, landing_page_qs_params,
                                            application_page_qs_params, landing_page_url):
            global landing_page_qs_param

            landing_page_qs = json.loads(landing_page_qs_params)
            application_page_qs = json.loads(application_page_qs_params)
            campaignid_in_qs = False
            is_matched = True
            if len(landing_page_qs) != 0 and len(application_page_qs) != 0:
                for i in landing_page_qs:
                    i = i.lower()
                    if i == 'campaignid':
                        campaignid_in_qs = True
                    landing_page_qs_param = [item.lower() for item in landing_page_qs[i]]
                    application_page_qs_param = [item.lower() for item in application_page_qs[i]]
                    input_value = ""
                    passed_value = ""
                    if landing_page_qs_param == application_page_qs_param:
                        key = i
                        for value in landing_page_qs[i]:
                            input_value += value
                        for value in application_page_qs[i]:
                            passed_value += value
                        line = "key: " + key + "\n" + "expected value: " + input_value + "\n" + "passed value: " + passed_value + "\n" + "Result: Matched" + "\n"
                        print(line)
                    else:
                        key = i
                        for value in landing_page_qs[i]:
                            input_value += value
                        for value in application_page_qs[i]:
                            passed_value += value
                        line = "key: " + key + "\n" + "expected value: " + input_value + "\n" + "passed value: " + passed_value + "\n" + "Result: Not matched (X)" + "\n"
                        print(line)
                        is_matched = False
            else:
                is_matched = False

            if is_matched:
                print("Query strings passed from the landing page are present in the cart page")
            else:
                print("Query strings parameters are not present in cart page from the landing page")

                """ email sending """

                subject = 'ALERT! Test Case Failed for Query Strings Parameters'
                body = "Query strings parameters are not present in cart page from the landing page " + landing_page_url

                self.send_email(subject, body)

                if campaignid_in_qs == False:
                    qs_value = self.qs_value_from_name(application_url, "campaignid")
                    key = "campaignid"
                    sub_string = self.get_sub_string_from_experience(experience_name)
                    if sub_string == "sem":
                        if page == 'join':
                            self.compare_values(key, Global_Env_Data.DEFAULT_SEM_JOIN_CAMPAIGN_ID, qs_value)
                        elif page == 'renew':
                            self.compare_values(key, Global_Env_Data.DEFAULT_SEM_RENEW_CAMPAIGN_ID, qs_value)
                    elif sub_string == "soc":
                        if page == 'join':
                            self.compare_values(key, Global_Env_Data.DEFAULT_SOC_JOIN_CAMPAIGN_ID, qs_value)
                        elif page == 'renew':
                            self.compare_values(key, Global_Env_Data.DEFAULT_SOC_RENEW_CAMPAIGN_ID, qs_value)
                    elif sub_string == "dis":
                        if page == 'join':
                            self.compare_values(key, Global_Env_Data.DEFAULT_DIS_JOIN_CAMPAIGN_ID, qs_value)
                        elif page == 'renew':
                            self.compare_values(key, Global_Env_Data.DEFAULT_DIS_RENEW_CAMPAIGN_ID, qs_value)
                    else:
                        if page == 'join':
                            self.compare_values(key, Global_Env_Data.DEFAULT_JOIN_CAMPAIGN_ID, qs_value)
                        elif page == 'renew':
                            self.compare_values(key, Global_Env_Data.DEFAULT_RENEW_CAMPAIGN_ID, qs_value)

    @staticmethod
    def get_browser(browser_type):
        if browser_type == Global_Env_Data.CHROME:
            chrome_path = ChromeDriverManager().install()
            ops = platform.system()
            if ops is not None and ops.lower() == 'linux':
               chrome_path = chrome_path
            else:
                chrome_path = chrome_path.split('/')[0] + '\chromedriver.exe'
                
            service = ChromeService(executable_path=chrome_path)
            #service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            
            if ops is not None and ops.lower() == 'linux':
                options.binary_location = '/opt/google/chrome/google-chrome'
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu")
            else:
                options.add_argument("--start-maximized")

            options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            return webdriver.Chrome(service=service, options=options)
            
        elif browser_type == Global_Env_Data.FIREFOX:
            firefox_driver = webdriver.Firefox()
            firefox_driver.maximize_window()
            return firefox_driver

    @staticmethod
    def get_template_csv_file() -> []:
        csv_file_contents = []
        # path_to_csv_file = Global_Env_Data.LOCAL_PATH + Global_Env_Data.MULTI_URLS
        path_to_csv_file = str(Path(os.getcwd())) + Global_Env_Data.MULTI_URLS
        with open(path_to_csv_file, mode='r') as csv_file:
            row_content = csv.reader(csv_file)
            for row in row_content:
                url = row[0]
                csv_file_contents.append(url)
        return csv_file_contents

    def open_browser(self, url, browser_type):
        driver = self.get_browser(browser_type)
        driver.get(url)
        # driver.maximize_window()
        return driver

    @staticmethod
    def close_browser(driver):
        # driver.delete_all_cookies()
        # driver.refresh()
        driver.quit()
        print("BROWSER CLOSED")

    def phone_number_verification(self, driver, url, phone_num_to_verify):
        value = driver.find_elements(By.CLASS_NAME, 'aarp-js-header-lp__phoneNumber')
        # if not value:
        #     value = driver.find_elements(By.XPATH, "//span[contains(@class,'aarp-js-header-lp__phoneNumber')]")
        for i in value:
            if i.is_displayed():
                headertext = i.get_attribute('innerText')
                if len(headertext) != 0:
                    if headertext == phone_num_to_verify:
                        print(headertext + " Correct phone number is displayed")
                        if (i.get_attribute('href') == ("tel:" + headertext)):
                            print("Phone number is clickable")
                        else:
                            print("Phone number is not clickable")
                            subject = 'ALERT! Test Case Phone number is not clickable'
                            body = headertext + " - Phone number is not clickable for the URL " + url
                            self.send_email(subject, body)
                    else:
                        print(headertext + ' Incorrect phone number is displayed')
                        subject = 'ALERT! Test Case Failed for header phone number'
                        body = headertext + " - Incorrect phone number is displayed in header for the URL " + url
                        self.send_email(subject, body)

    def click_join_button(self, driver):
        is_visible = self.is_visible(driver, self.Button_Click_Header_Join)
        assert is_visible == True, "The Button is not visible"
        print("Clicked on JOIN header button")
        self.button_click(driver, self.Button_Click_Header_Join)
        print("Navigated to Application page \n")

    def click_renew_button(self, driver):
        is_visible = self.is_visible(driver, self.Button_Click_Header_Renew)
        assert is_visible == True, "The Button is not visible"
        print("Clicked on RENEW header button")
        self.button_click(driver, self.Button_Click_Header_Renew)
        print("Navigated to find me page \n")

    def qs_value_from_name(self, url, name):
        try:
            qs_value = parse_qs(urlparse(url).query)[name][0]
            return qs_value
        except KeyError:
            print('Can not find "' + name + '"')
            return "null"

    def qs_as_json_object(self, url):
        try:
            _qs_json_obj = json.dumps(parse_qs(urlparse(url).query))
            return _qs_json_obj
        except KeyError:
            print('Can not get the query string json objects')
            return "null"

    def qs_as_json_object_pyp(self, url):
        try:
            # _qs_json_obj = json.dumps(parse_qs(urlparse(url).query))
            _qs_json_obj = json.dumps(parse_qs(urlparse(url).query, keep_blank_values=True))
            return _qs_json_obj
        except KeyError:
            print('Can not get the query string json objects')
            return "null"

    def compare_qs_values(self, key, expected_value, passed_value):
        self.compare_values(key, expected_value, passed_value)

    def compare_all_qs_params_in_json(self, experience_name, application_url, landing_page_qs_params,
                                      application_page_qs_params, landing_page_url, button_type):
        self.compare_query_string_parameters(button_type, experience_name, application_url, landing_page_qs_params,
                                             application_page_qs_params, landing_page_url)

    def send_email(self, subject, body):
        mail = EmailMessage()
        mail['From'] = formataddr((Global_Env_Data.EMAIL_SENDER_NAME, Global_Env_Data.EMAIL_SENDER))
        mail['To'] = Global_Env_Data.EMAIL_RECEIVER
        mail['subject'] = subject
        mail.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_PASSWORD)
            smtp.sendmail(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_RECEIVER, mail.as_string())
        print("EMAIL SENT")

    def image_compare(self):
        try:
            image1 = cv2.imread(Global_Env_Data.IMAGE_FILE_PATH + 'input_image.png')
            image2 = cv2.imread(Global_Env_Data.IMAGE_FILE_PATH + 'browser_screenshot.png')
            difference = cv2.absdiff(image1, image2)

            # Convert difference to grayscale
            Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

            # ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_TRIANGLE)
            cv2.imwrite(Global_Env_Data.IMAGE_FILE_PATH + 'img_diff_grey.png', Conv_hsv_Gray)
            # add the green mask to the image to show the differences
            image1[mask != 255] = [0, 255, 0]

            status = cv2.imwrite(Global_Env_Data.IMAGE_FILE_PATH + 'img_mask.png', image1)
            image_diff = cv2.imread(Global_Env_Data.IMAGE_FILE_PATH + 'img_mask.png')
            # concat_diff2 = np.concatenate((image_diff, image1), axis=1)
            # status = cv2.imwrite(Global_Env_Data.IMAGE_FILE_PATH + 'concat_img.png', concat_diff2)
            print("End of image_compare====================")
        except Exception as e:
            print("exception from img compare " + str(e))

    def image_to_pdf(self):
        try:
            report_img_path = Global_Env_Data.IMAGE_FILE_PATH + 'img_mask.png'
            print(report_img_path)
            report_img_pdf_path = "static/pdf/" + 'image_diff_pdf.pdf'
            print(report_img_pdf_path)
            image = Image.open(report_img_path)
            pdf_bytes = img2pdf.convert(image.filename)
            file = open(report_img_pdf_path, "wb")
            file.write(pdf_bytes)
            image.close()
            file.close()
        except Exception as e:
            print("exception from img tp pdf compare " + str(e))

    def chrome_compare(self, url):
        image1 = cv2.imread(Global_Env_Data.IMAGE_FILE_PATH + 'input_image.png')
        print(image1.shape)
        width = image1.shape[1]
        height = image1.shape[0]
        service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        time.sleep(5)
        print("After options declared")
        options.add_argument("--headless")
        options.binary_location = '/opt/google/chrome/google-chrome'
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(5)
        driver.get(url)
        time.sleep(20)
        driver.save_screenshot(Global_Env_Data.IMAGE_FILE_PATH + 'browser_screenshot.png')
        time.sleep(2)
        driver.close()

    def run_image_comparison(self, url):
        try:
            # self.remove_image_file()
            print(url)
            self.chrome_compare(url)
            time.sleep(5)
            self.image_compare()
            time.sleep(2)
            self.image_to_pdf()
        except Exception as e:
            print("Exception from run_image_comparison" + str(e))

    def remove_image_file(self):
        print("inside remove_image_file")
        files = glob.glob(os.path.abspath(Global_Env_Data.IMAGE_FILE_PATH + '*.*'))
        for f in files:
            os.remove(f)