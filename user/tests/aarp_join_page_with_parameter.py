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

    def page_url(self):
        return self.get_url()

    def host_name(self, url):
        return self.get_hostname(url)

    def path_name(self, url):
        path = self.get_path(url).replace("/", "")
        return path

    def click_join_button(self):
        is_visible = self.is_visible(self.Button_Click_Header_Join)
        assert is_visible == True, "The Button is not visible"
        print("Clicked on JOIN header button")
        self.button_click(self.Button_Click_Header_Join)
        print("Navigated to Application page \n")

    def qs_value_from_name(self, url, name):
        qs_value = self.get_qs_value_by_name(url, name)
        return qs_value

    def qs_as_json_object(self, url):
        qs_json_object = self.get_qs_json_object(url)
        return qs_json_object

    def compare_qs_values(self, key, expected_value, passed_value):
        self.compare_values(key, expected_value, passed_value)

    def compare_all_qs_params_in_json(
        self,
        experience_name,
        application_url,
        landing_page_qs_params,
        application_page_qs_params,
        landing_page_url,
    ):
        self.compare_query_string_parameters(
            "join",
            experience_name,
            application_url,
            landing_page_qs_params,
            application_page_qs_params,
            landing_page_url,
        )
