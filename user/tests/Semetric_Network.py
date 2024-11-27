import smtplib
import ssl
from email.message import EmailMessage
from user.Config.config import Global_Env_Data

from user.tests.template_class import TemplateClass
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time
import json
from urllib.parse import parse_qs

class SemetricNetwork(TemplateClass):
    global vsixtytesting
    global networkvsixty
    vsizty = False
    vonenineseven = False
    v60Present = False
    check_campaign_tc = ''
    check_campaignid = ''
    def main_functionality(self,log_entries,driver,url,execute_network_logs,parsed_url):
        self.check_campaignid = ''
        #self.tc_campaignid = ''
        self.tc_campaign = ''
        self.tc_camp_present = False
        self.check_tc_campaign = False
        #self.check_tc_campaignid = False
        time.sleep(6)
        try:
            parsed_url = (urlparse(parsed_url))
            self.check_campaignid = parse_qs(parsed_url.query)['campaignid'][0]
            print("campaignid parameter is present in query string : ", self.check_campaignid)
        except:
            print("campaignid parameter checking ")

            #print("campaignid parameter is not present ")
            get_join_button = driver.find_element(By.CLASS_NAME, 'aarp-js-lp--joinNow')
            join_href = get_join_button.get_attribute("href")
            parsed_url = (urlparse(join_href))
            self.check_campaignid = parse_qs(parsed_url.query)['campaignid'][0]
            self.check_campaignid = self.check_campaignid.lower()

        for item in execute_network_logs:
            try:
                networkvsixty = parse_qs(urlparse(item["name"]).query)['v60'][0]
                vsixtytesting = True
                if  self.check_campaignid.lower() == networkvsixty.lower():
                    print("\ncampaignid : " + self.check_campaignid.lower()  + " and v60:" + networkvsixty.lower() + " are matched")
                break
            except KeyError:
                vsixtytesting = False
                pass
        if vsixtytesting != True:
           SemetricNetwork.extract_from_logs(self,"v60",log_entries,self.check_campaignid)
        try:
            self.check_tc_campaign = parse_qs(parsed_url.query)['tc_campaign'][0]
            print("\ntc_campaign parameter is present in query string: ", self.check_tc_campaign)
            self.tc_camp_present = True
        except:
            print("tc_campaign parameter is not present")

            """ email sending if issues there in Smetric Network """
            subject = 'ALERT! Test Case Failed for Smetric Network'
            body = 'tc_campaign' + " parameter is not present in the URL " + url

            em = EmailMessage()
            em['From'] = Global_Env_Data.EMAIL_SENDER
            em['To'] = Global_Env_Data.EMAIL_RECEIVER
            em['subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_PASSWORD)
                smtp.sendmail(Global_Env_Data.EMAIL_SENDER, Global_Env_Data.EMAIL_RECEIVER, em.as_string())

            self.tc_camp_present = False
            
        for item in execute_network_logs:
            try:
                networkone_ninty_seven = parse_qs(urlparse(item["name"]).query)['v197'][0]
                vonenintyseventesting = True
                if self.check_tc_campaign.lower() == networkone_ninty_seven.lower():
                    print("tc_campaign : " + self.check_tc_campaign.lower() + " and v197: " + networkone_ninty_seven.lower() + " are matched")
                break
            except KeyError:
                vonenintyseventesting = False
                pass
        if vonenintyseventesting != True  and self.tc_camp_present == True:
            SemetricNetwork.extract_from_logs(self,"v197",log_entries,self.check_tc_campaign)

    def extract_from_logs(self, value,log_entries,campaignid):
        extracted_value = ''
        networkparamoccurence = False
        for entry in log_entries:
            try:
                message_obj = json.loads(entry.get("message"))
                message = message_obj.get("message")
                method = message.get("method")
                if method == 'Network.requestWillBeSent':
                    request_url = message.get('params', {}).get('request', {}).get('url', '')
                    request_payload = message.get('params', {}).get('request', {}).get('postData', {})
                    if ("smetrics" in request_url) and (len(request_payload) != 0):
                        try:
                            extracted_value = parse_qs(request_payload)[value][0]
                            networkparamoccurence = True
                            break
                        except KeyError:
                            networkparamoccurence = False
            except Exception as e:
                print(e)
        if value == "v60":
            if (extracted_value.lower() == campaignid.lower()) :
                print("\ncampaignid : " + campaignid.lower() + " and v60:" + extracted_value.lower() + " are matched")
            else:
                print("v60 value is not present")
        if value == "v197":
            if (extracted_value.lower() == campaignid.lower()):
                print("\ntc_campaign : "+ campaignid.lower() + " and v197: " + extracted_value.lower() + " are matched")
            else:
                print("\nv197 value is not present")
        return (extracted_value, networkparamoccurence)
