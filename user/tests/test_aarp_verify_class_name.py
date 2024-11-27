import ssl
import smtplib
import time, pytest, sys
from email.message import EmailMessage
from user.Config.config import Global_Env_Data
from user.tests.common_functions import TestCommonFunctions
from selenium.webdriver.common.by import By


class TestAarpVerifyClassName:
    @pytest.mark.nondestructive
    def test_run_test_case(self):
        print("TEST CASE BEGIN - AARP CLASS NAMES")
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
                self.perform_test_steps(driver, base_url)
            except Exception as e:
                print(f"AN ERROR OCCURRED IN TEST - CLASS NAMES: {e}")
            finally:
                self.common_functions.close_browser(driver)
        else:
            for url in self.csv_contents:
                print("TESTING THE URL: " + url)
                driver = self.common_functions.open_browser(url, Global_Env_Data.CHROME)
                time.sleep(5)
                try:
                    self.perform_test_steps(driver, url)
                except Exception as e:
                    print(f"AN ERROR OCCURRED IN TEST - CLASS NAMES: {e}")
                finally:
                    self.common_functions.close_browser(driver)

    def send_mail(self, url, count):
        self.common_functions = TestCommonFunctions()
        self.count = ""
        messageBody = ""
        for i in count:
            if i and (i.__contains__("__")):
                messageBody = (
                    messageBody
                    + "For the class name "
                    + '"'
                    + i.strip()
                    + '"'
                    + ",the class declaration not as per the BEM naming for the URL  "
                    + url
                    + "\n"
                )
            else:
                messageBody = (
                    messageBody
                    + "For the class name "
                    + '"'
                    + i.strip()
                    + '"'
                    + ",the class declaration not as per the BEM naming for the URL "
                    + url
                    + "\n"
                )

        print("Sending the mail")
        subject = "ALERT! Test Case Failed for class name"
        body = messageBody
        self.common_functions.send_email(subject, body)

    def Convert(self, string):
        li = list(string.split(" "))
        return li

    def perform_test_steps(self, driver, url, VALUE_TO_FIND=None, all_classnames=None):
        print("PERFORM CLASS NAMES TEST STEPS START")
        # self.full_page_screenshot_lp = lambda x: driver.execute_script(
        #     'return document.body.parentNode.scroll' + x)
        # driver.set_window_size(self.full_page_screenshot_lp('Width'),
        #                             self.full_page_screenshot_lp('Height'))  # May need manual adjustment
        # driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot.png')
        # #driver.find_element("tag name", "body").screenshot('user/static/reports/html/screenshot/onload_screenshot_' + url.split('/')[4] + '.png')
        time.sleep(5)
        all_classnames_1 = driver.find_elements(By.TAG_NAME, "a")
        all_classnames_2 = driver.find_elements(By.TAG_NAME, "span")
        all_classnames_3 = driver.find_elements(By.TAG_NAME, "div")
        all_classnames_4 = driver.find_elements(By.TAG_NAME, "p")
        all_classnames = []
        all_classnames.extend(all_classnames_1)
        all_classnames.extend(all_classnames_2)
        all_classnames.extend(all_classnames_3)
        all_classnames.extend(all_classnames_4)
        self.count = []
        for classname in all_classnames:
            text_find = classname.get_attribute("class")
            list_val = self.Convert(text_find)
            for i in list_val:
                if len(i) != 0:
                    if (
                        i
                        and ((i.__contains__("aarp-")) and len(i) != 0)
                        or (i.__contains__("button"))
                        or (i.__contains__("aarpHeaderButton"))
                        or (i.__contains__("aem-"))
                        or (i.__contains__("svgTag"))
                        or (i.__contains__("sharp-c-"))
                        or (i.__contains__("icon-incorrect"))
                        or (i.__contains__("cmp-"))
                        or (i.__contains__("header"))
                        or (i.__contains__("hpHeader"))
                        or (i.__contains__("Living"))
                        or (i.__contains__("Auto"))
                        or (i.__contains__("Staying"))
                        or (i.__contains__("Sharp"))
                        or (i.__contains__("Podcasts"))
                        or (i.__contains__(""))
                        or (i.__contains__("lazyload"))
                        or (i.__contains__("embed"))
                        or (i.__contains__("uxdia"))
                        or (i.__contains__("section"))
                        or (i.__contains__("target"))
                        or (i.__contains__("headerSearchToOpenModal"))
                        or (i.__contains__("&"))
                        or (i.__contains__("Social"))
                        or (i.__contains__("Work"))
                        or (i.__contains__("Entertainment"))
                        or (i.__contains__("footer-"))
                        or (i.__contains__("image"))
                        or (i.__contains__("advancedhtml"))
                        or (i.__contains__("combo"))
                        or (i.__contains__("js"))
                        or (i.__contains__("promoHeader"))
                        or (i.__contains__("ghost"))
                        or (i.__contains__("campaign"))
                        or (i.__contains__("responsivegrid"))
                        or (i.__contains__("magzine_join"))
                        or (i.__contains__("option"))
                        or (i.__contains__("coreHeader"))
                        or (i.__contains__("xf"))
                        or (i.__contains__("we"))
                        or (i.__contains__("Videos"))
                        or (i.__contains__("Tech"))
                        or (i.__contains__("Relationships"))
                        or (i.__contains__("coreFooter"))
                        or (i.__contains__("experiencefragment"))
                        or (i.__contains__("articleimage"))
                        or (i.__contains__("hero-"))
                        or (i.__contains__("navigationLinks"))
                        or (i.__contains__("Health"))
                        or (i.__contains__("Money"))
                        or (i.__contains__("Jobs"))
                        or (i.__contains__("Security"))
                        or (i.__contains__("Medicare"))
                        or (i.__contains__("Caregiving"))
                        or (i.__contains__("Games"))
                        or (i.__contains__("footerQuickLink"))
                        or (i.__contains__("parbase"))
                        or (i.__contains__("featuredTile"))
                        or (i.__contains__("container"))
                        or (i.__contains__("root"))
                        or (i.__contains__("showPromoHeader"))
                        or (i.__contains__("Travel"))
                        or (i.__contains__("More"))
                        or (i.__contains__("Style"))
                        or (i.__contains__("Family"))
                        or (i.__contains__("Personal"))
                        or (i.__contains__("Home"))
                        or (i.__contains__("page-"))
                        or (i.__contains__("herobanner-right-js"))
                        or (i.__contains__("heroRightLogoBox-lp-js"))
                        or (i.__contains__("col"))
                        or (i.__contains__("flex"))
                        or (i.__contains__("card"))
                        or (i.__contains__("row"))
                        or (i.__contains__("infiniteslide_wrap"))
                        or (i.__contains__("travel"))
                        or (i.__contains__("shoppingandgroceries"))
                        or (i.__contains__("autoservice"))
                        or (i.__contains__("healthandwellness"))
                        or (i.__contains__("entertainment"))
                        or (i.__contains__("restaurants"))
                        or (i.__contains__("finances"))
                        or (
                            i.__contains__("insurance")
                            or (i.__contains__("homeandfamily"))
                            or (i.__contains__("caregiving"))
                            or (i.__contains__("workandjobs"))
                            or (i.__contains__("community"))
                            or (i.__contains__("magazine"))
                            or (i.__contains__("advocacy"))
                            or (i.__contains__("technologyandwireless"))
                            or (i.__contains__("search"))
                            or (i.__contains__("close"))
                            or (i.__contains__("vjs"))
                            or (i.__contains__("icon"))
                            or (i.__contains__("formcontent"))
                            or (i.__contains__("aos-init"))
                            or (i.__contains__("notaarp_outback"))
                            or (i.__contains__("des_dis"))
                            or (i.__contains__("bottom_textSec"))
                            or (i.__contains__("aos-"))
                            or (i.__contains__("expJoinButn"))
                            or (i.__contains__("memautorenew"))
                            or (i.__contains__("slick-"))
                            or (i.__contains__("draggable"))
                            or (i.__contains__("mob_dis"))
                            or (i.__contains__("dynPremium1"))
                            or (i.__contains__("text"))
                        )
                    ):
                        pass
                    else:
                        self.count.append(i)
        print(self.count)
        if len(self.count) != 0:
            self.send_mail(url, self.count)
        print("Classnames followed https://getbem.com/naming/ is correct.")
        print("PERFORM CLASS NAMES TEST STEPS END")
