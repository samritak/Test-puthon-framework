from email.message import EmailMessage

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import re
from user.Config.config import Global_Env_Data
from selenium.webdriver.common.by import By
import smtplib
from email.message import EmailMessage
import ssl
import time

"""
Parent for all pages
"""
"""
"""


class TemplateClass:
    def __init__(self, driver):
        self.driver = driver

    """
    Get the title of the corresponding opened page 
    :return value _title
    """

    def get_title(self):
        _title = self.driver.title
        return _title

    """
    Get the text from the corresponding given locator.
    :return _get_text_value
    """

    def get_text(self, by_locator):
        _get_text_value = self.driver.find_element(by_locator).text
        return _get_text_value

    """
     Click the button based on given locator
     :return bool(_clicked)
    """

    def button_click(self, by_locator):
        _clicked = WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable(by_locator)
        )
        _clicked.click()
        return bool(_clicked)

    """
    Send the input value to the given locator along with the value
    :return bool(_send_keys)
    """

    def send_text_keys(self, by_locator, text):
        _send_keys = WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable(by_locator)
        )
        _send_keys.send_keys(text)
        return bool(_send_keys)

    """
    Check the given locator is visible or not on the page.
    :return bool(_element_present)
    """

    def is_visible(self, by_locator):
        _element_present = WebDriverWait(self.driver, 20).until(
            ec.visibility_of_element_located(by_locator)
        )
        return bool(_element_present)

    """
    Check the visibility of the given locator (section) on the page.
    :return bool(_check_element_present_value)
    """

    def check_element_presence(self, by_locator):
        _check_element_present_value = WebDriverWait(self.driver, 20).until(
            ec.visibility_of_element_located(by_locator)
        )
        return bool(_check_element_present_value)

    """
    Scroll the page to the specific locator(section) on the page.
    :return null
    """

    def scroll_page_to_element(self, by_locator):
        print("scrolling page.........")
        self.element = WebDriverWait(self.driver, 20).until(
            ec.visibility_of_element_located(by_locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)

    """
    Get the URL of a current opened page 
    :return value _url
    """

    def get_url(self):
        _url = self.driver.current_url
        return _url

    """
    Check the query string present in the given URL 
    :return value True or False
    """

    @staticmethod
    def check_query_string_present(url):
        _parsed_qs = parse_qs(urlparse(url).query)
        if _parsed_qs:
            print("Query string are present in the URL \n")
            return True
        else:
            print("Query string not present in the landing page \n")
            return False

    """
    Get host name from given URL 
    :return value _hostname
    """

    @staticmethod
    def get_hostname(url):
        parsed_url = urlparse(url)
        _hostname = parsed_url.hostname
        return _hostname

    """
    Get host name from given URL 
    :return value _path
    """

    @staticmethod
    def get_path(url):
        parsed_url = urlparse(url)
        _path = parsed_url.path
        return _path

    """
    Get the query string value from the url for a specific key name
    :return value _qs_value or null
    """

    @staticmethod
    def get_qs_value_by_name(url, key_name):
        try:
            _qs_value = parse_qs(urlparse(url).query)[key_name][0]
            return _qs_value
        except KeyError:
            print('Can not find "' + key_name + '"')
            return "null"

    @staticmethod
    def get_qs_json_object(url):
        try:
            _qs_json_obj = json.dumps(parse_qs(urlparse(url).query))
            return _qs_json_obj
        except KeyError:
            print('Can not find "' + url + '"')

            return "null"

    def compare_values(self, key, expected_value, passed_value):
        if expected_value == passed_value:
            line = (
                "key: "
                + key
                + "\n"
                + "expected value: "
                + expected_value
                + "\n"
                + "passed value: "
                + passed_value
                + "\n"
                + "Result: Matched"
                + "\n"
            )
            print(line)
        else:
            line = (
                "key: "
                + key
                + "\n"
                + "expected value: "
                + expected_value
                + "\n"
                + "passed value: "
                + passed_value
                + "\n"
                + "Result: Not matched (X)"
                + "\n"
            )
            print(line)

    @staticmethod
    def get_sub_string_from_experience(experience_name):
        if (
            re.search("^sem-", experience_name)
            or re.search("-sem-", experience_name)
            or re.search("-sem$", experience_name)
        ):
            return "sem"
        elif (
            re.search("^soc-", experience_name)
            or re.search("-soc-", experience_name)
            or re.search("-soc$", experience_name)
        ):
            return "soc"
        elif (
            re.search("^dis-", experience_name)
            or re.search("-dis-", experience_name)
            or re.search("-dis$", experience_name)
        ):
            return "dis"
        else:
            return "default"

    def compare_query_string_parameters(
        self,
        page,
        experience_name,
        application_url,
        landing_page_qs_params,
        application_page_qs_params,
        landing_page_url,
    ):
        global landing_page_qs_param
        landing_page_qs = json.loads(landing_page_qs_params)
        application_page_qs = json.loads(application_page_qs_params)
        campaignid_in_qs = False
        for i in landing_page_qs:
            if i == "campaignid":
                campaignid_in_qs = True
            landing_page_qs_param = [item.lower() for item in landing_page_qs[i]]
            application_page_qs_param = [
                item.lower() for item in application_page_qs[i]
            ]
            if landing_page_qs_param == application_page_qs_param:
                key = i
                input_value = ""
                passed_value = ""
                for value in landing_page_qs[i]:
                    input_value += value
                for value in application_page_qs[i]:
                    passed_value += value
                line = (
                    "key: "
                    + key
                    + "\n"
                    + "expected value: "
                    + input_value
                    + "\n"
                    + "passed value: "
                    + passed_value
                    + "\n"
                    + "Result: Matched"
                    + "\n"
                )
                print(line)
            else:
                key = i
                line = (
                    "key: "
                    + key
                    + "\n"
                    + "expected value: "
                    + input_value
                    + "\n"
                    + "passed value: "
                    + passed_value
                    + "\n"
                    + "Result: Not matched (X)"
                    + "\n"
                )
                print(line)

            """ comparison  of landing page query string and cart page query string """

            landing_page_qs = json.loads(landing_page_qs_params)
            application_page_qs = json.loads(application_page_qs_params)
        if landing_page_qs == application_page_qs:
            print(
                "Query strings passed from the landing page are present in the cart page"
            )
        else:
            print(
                "Query strings parameters are not present in cart page from the landing page"
            )

            """ email sending """

            subject = "ALERT! Test Case Failed for Query Strings Parameters"
            body = (
                "Query strings parameters are not present in cart page from the landing page "
                + landing_page_url
            )

            em = EmailMessage()
            em["From"] = Global_Env_Data.EMAIL_SENDER
            em["To"] = Global_Env_Data.EMAIL_RECEIVER
            em["subject"] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_PASSWORD)
                smtp.sendmail(
                    Global_Env_Data.EMAIL_SENDER,
                    Global_Env_Data.EMAIL_RECEIVER,
                    em.as_string(),
                )

        if campaignid_in_qs == False:
            qs_value = self.get_qs_value_by_name(application_url, "campaignid")
            key = "campaignid"
            sub_string = self.get_sub_string_from_experience(experience_name)
            if sub_string == "sem":
                if page == "join":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_SEM_JOIN_CAMPAIGN_ID, qs_value
                    )
                elif page == "renew":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_SEM_RENEW_CAMPAIGN_ID, qs_value
                    )
            elif sub_string == "soc":
                if page == "join":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_SOC_JOIN_CAMPAIGN_ID, qs_value
                    )
                elif page == "renew":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_SOC_RENEW_CAMPAIGN_ID, qs_value
                    )
            elif sub_string == "dis":
                if page == "join":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_DIS_JOIN_CAMPAIGN_ID, qs_value
                    )
                elif page == "renew":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_DIS_RENEW_CAMPAIGN_ID, qs_value
                    )
            else:
                if page == "join":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_JOIN_CAMPAIGN_ID, qs_value
                    )
                elif page == "renew":
                    self.compare_values(
                        key, Global_Env_Data.DEFAULT_RENEW_CAMPAIGN_ID, qs_value
                    )

    def find_default_premium(self):
        premium1 = self.driver.find_element(By.CLASS_NAME, "dynPremium1")
        premium2 = self.driver.find_element(By.CLASS_NAME, "dynPremium2")

        # Get the value of the data-sku attribute
        # data_sku = pr1.get_attribute('data-jkc1')
        class_name1 = premium1.get_attribute("class")
        class_name2 = premium2.get_attribute("class")

        # Find the element you want to check the selected class on
        if "active" in class_name1:
            default_premium = "premium1"
        elif "active" in class_name2:
            default_premium = "premium2"

        return default_premium

    def find_default_campaignid(self, premium, flow):
        premium1 = self.driver.find_element(By.CLASS_NAME, "dynPremium1")
        premium2 = self.driver.find_element(By.CLASS_NAME, "dynPremium2")

        # Get the value of the data-sku attribute
        if premium == "premium1":
            if flow == "jkc":
                campaign_id = premium1.get_attribute("data-jkc1")
            elif flow == "rkc":
                campaign_id = premium1.get_attribute("data-rkc1")
        elif premium == "premium2":
            if flow == "jkc":
                campaign_id = premium2.get_attribute("data-jkc2")
            elif flow == "rkc":
                campaign_id = premium2.get_attribute("data-rkc2")

        return campaign_id

    def compare_query_string_parameters_for_pyp(
        self, landing_page_qs_params, application_page_qs_params
    ):
        landing_page_qs = json.loads(landing_page_qs_params)
        application_page_qs = json.loads(application_page_qs_params)
        for i in landing_page_qs:
            if (
                i != "campaignid"
                and i != "jkc1"
                and i != "jkc2"
                and i != "rkc1"
                and i != "rkc2"
            ):
                if landing_page_qs[i] == application_page_qs[i]:
                    key = i
                    input_value = ""
                    passed_value = ""
                    for value in landing_page_qs[i]:
                        input_value += value
                    for value in application_page_qs[i]:
                        passed_value += value
                    line = (
                        "key: "
                        + key
                        + "\n"
                        + "expected value: "
                        + input_value
                        + "\n"
                        + "passed value: "
                        + passed_value
                        + "\n"
                        + "Result: Matched"
                        + "\n"
                    )
                    print(line)
                else:
                    line = (
                        "key: "
                        + key
                        + "\n"
                        + "expected value: "
                        + input_value
                        + "\n"
                        + "passed value: "
                        + passed_value
                        + "\n"
                        + "Result: Not matched (X)"
                        + "\n"
                    )
                    print(line)
