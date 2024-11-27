import time

from user.tests.template_class import TemplateClass
from selenium.webdriver.common.by import By


class JoinPage(TemplateClass):
    Button_Click_Header_Join = (By.XPATH, '//*[@id="head_jn"]')

    """
    Get the url's from the pageurls.csv page and open it.
    """

    def __init__(self, driver, url):
        super().__init__(driver)
        self.driver.get(url)
        self.driver.maximize_window()

    def page_title(self):
        return self.get_title()

    def page_url(self):
        return self.get_url()

    def host_name(self, url):
        return self.get_hostname(url)

    def path_name(self, url):
        path = self.get_path(url).replace("/", "")
        return path

    def query_string_present(self, url):
        query_string_present = self.check_query_string_present(url)
        assert (
            query_string_present == False
        ), "Query string should not present in the given input URL"

    def click_join_button(self):
        is_visible = self.is_visible(self.Button_Click_Header_Join)
        assert is_visible == True, "The Button is not visible"
        print("Clicked on JOIN header button")
        self.button_click(self.Button_Click_Header_Join)
        print("Navigated to Application page \n")

    def qs_value_from_name(self, url, name):
        qs_value = self.get_qs_value_by_name(url, name)
        return qs_value

    def search_name(self, experience_name):
        sub_string = self.get_sub_string_from_experience(experience_name)
        return sub_string

    def compare_qs_values(self, key, expected_value, passed_value):
        self.compare_values(key, expected_value, passed_value)
