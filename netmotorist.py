# system
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException


class NetMotorist(WebDriver):
    """
    This class is the exact WebDriver but with few more functions for this project usage
    """
    pass

    def refresh_loop(self, part_of_title, timeout, max_tries, no_internet_quit=True):
        """
        refreshes the driver until it in the right place or timeout

        :param no_internet_quit: quit when there is no internet exception
        :param max_tries: max tries
        :param timeout: the timeout between every refresh
        :param part_of_title: part of the title that is desired
        :return:
        """
        tries_count = 0
        while part_of_title not in self.title:
            sleep(timeout)
            self.refresh()
            tries_count += 1
            if tries_count >= max_tries:
                if (self.on_no_internet_page()):
                    if no_internet_quit:
                        self.quit()
                    raise NoInternetPageException
                else:
                    raise UnexpectedTitle

    def select_stuff(self, attribute, value):
        select_script_js = """
                const change_ev = new Event("change");
                const {attribute}_name = document.querySelector('#{attribute}');
                {attribute}_name.value = "{value}";
                {attribute}_name.dispatchEvent(change_ev);
                """.format(attribute=attribute, value=value)
        self.execute_script(select_script_js)

        sleep(3)

    def on_no_internet_page(self):
        try:
            main_message_text = self.find_element_by_xpath('//*[@id="main-message"]/h1/span').text.lower()
            if (main_message_text == "no internet" or
                main_message_text == "your connection was interrupted"):
                return True
        except NoSuchElementException:
            pass
        return False


class NetMotoristException(WebDriverException):
    """
    base custom exception for the webdriver
    """
    pass


class NoInternetPageException(NetMotoristException):
    """
    if on no-internet page
    """
    pass


class UnexpectedTitle(NetMotoristException):
    """
    if on a different page than expected
    """
    pass
