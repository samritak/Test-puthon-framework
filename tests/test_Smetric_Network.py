from pathlib import Path
from test_Template import BaseTemplate
from user.Config.config import Global_Env_Data
import csv,json, pytest, sys
from email.message import EmailMessage
import ssl,smtplib,os
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from JoinPage_WithoutParameter import JoinPage
import logging

class TestSmetricNetwork(BaseTemplate):
    @pytest.mark.nondestructive
    def test_join(self):
        self.driver.quit()
        self.contents = []
        # path_to_file = Global_Env_Data.LOCAL_PATH + Global_Env_Data.TEMPLATE_SMETRIC_NETWORK
        #path_to_file = str(Path(os.getcwd()).parent.absolute()) + Global_Env_Data.multiURls
        path_to_file = os.getcwd() + Global_Env_Data.multiURls
        base_url = sys.argv[2].split("--base-url=")[1]
        print(base_url)
        if base_url != 'None':
            try:
                print("TESTING THE URL: " + base_url)
                driver = self.common_functions.open_browser(base_url, Global_Env_Data.CHROME)
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - AARP PAGE SMETRIC: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            with open(path_to_file, mode='r') as file:
                cp_url = csv.reader(file)
                for row in cp_url:
                    url = row[0]
                    self.contents.append(url)

                for url in self.contents:
                    print("Testing the below URL")
                    print(url)
                    self.web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                    #self.join_page = JoinPage(self.driver, url)

                    # Perform the test steps
                    self.perform_test_steps(self.web_driver, url)

                    # Clear cookies and refresh the page
                    self.web_driver.delete_all_cookies()
                    print("Cookies cleared")
                    self.web_driver.refresh()

                    print("URL testing completed.")
                    print("\n")

                print("********* END OF REPORT *********")
                print("\n")

                self.web_driver.quit()

    def perform_test_steps(self, driver, url):
        logging.getLogger('seleniumwire').setLevel(logging.WARNING)
        # Go to the Google home page
        driver.get(url)
        driver.maximize_window()
        params = []
        # Access requests via the `requests` attribute
        parameters = []
        for re in driver.requests:
            if ("smetrics" in re.url):
                parameters.append(re.params)
                # print(re.url)
                #print(re.params)

        # the result is a Python dictionary:
        for i in parameters:
            string_Val_new = ""
            string_Val = str(i)
            for i in string_Val:
                # print(i)
                if (i == "\'"):
                    # print(i)
                    string_Val.replace((i), "\"")
                    # new_String= string_Val
                    # print(new_String,"new string")
                    string_Val_new = string_Val.replace((i), "\"")
            #print(string_Val_new)
            jsonval = json.loads(string_Val_new)
            # try block
        try:
            print("V60 parameter value is " + jsonval["v60"])
            # break
            # except Block
        except KeyError:
            print("v60 parameter value is not present")
            self.send_mail("v60 not present in network tab smetric", url)

        try:
            print(jsonval["v197"])
            # break
            # except Block
        except KeyError:
            print("v197 parameter value is not present")
            self.send_mail("v197 not present in network tab smetric", url)

    def send_mail(self, error_message, url):
        subject = 'ALERT! Test Case Failed for Smetric Network'
        body = error_message + " URL: " + url
        em = EmailMessage()
        em['From'] = Global_Env_Data.EMAIL_SENDER
        em['To'] = Global_Env_Data.EMAIL_RECEIVER
        em['subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_PASSWORD)
            smtp.sendmail(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_RECEIVER, em.as_string())