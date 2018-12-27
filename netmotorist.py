# system
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException


class NetMotorist(WebDriver):
    drivers_count = 0
    """
    This class is the exact WebDriver but with few more functions for this project usage
    """

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True):
        NetMotorist.drivers_count += 1
        if NetMotorist.drivers_count >= 10:
            raise MemoryError("too many open drivers")

        super(NetMotorist, self).__init__(
                executable_path, port,
                 options, service_args,
                 desired_capabilities, service_log_path,
                 chrome_options, keep_alive)

    def quit(self):
        NetMotorist.drivers_count -= 1
        super(NetMotorist, self).quit()

    def refresh_loop(self, part_of_title, timeout=3, max_tries=3, no_internet_quit=True):
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
                    raise UnexpectedPage

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

    def save_find_element_by_id(self, id_, timeout=3, max_tries=3, no_internet_quit=True):
        """
        the same as find element by id, but this one refreshes the page if it don't work
        :return:
        """
        elem = None
        for i in xrange(max_tries):
            try:
                elem = self.find_element_by_id(id_)
                break
            except NoSuchElementException:
                self.refresh()
                sleep(timeout)

        if elem is not None:
            return elem

        if self.on_no_internet_page():
            if no_internet_quit:
                self.quit()
            raise NoInternetPageException
        else:
            # return the actual error message
            return self.find_element_by_id(id_)


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


class UnexpectedPage(NetMotoristException):
    """
    if on a different page than expected
    """
    pass
