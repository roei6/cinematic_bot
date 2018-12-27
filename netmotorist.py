# system
from time import sleep
from selenium.webdriver.chrome.webdriver import WebDriver


class NetMotorist(WebDriver):
    """
    This class is the exact WebDriver but with few more functions for this project usage
    """
    pass

    def refresh_loop(self, part_of_title, timeout, max_tries):
        """
        refreshes the driver until it in the right place or timeout
        :param driver:
        :return:
        """
        tries_count = 0
        while part_of_title not in self.title:
            sleep(timeout)
            self.refresh()
            tries_count += 1
            if tries_count >= max_tries:
                raise Exception

    def select_stuff(self, attribute, value):
        select_script_js = """
                const change_ev = new Event("change");
                const {attribute}_name = document.querySelector('#{attribute}');
                {attribute}_name.value = "{value}";
                {attribute}_name.dispatchEvent(change_ev);
                """.format(attribute=attribute, value=value)
        self.execute_script(select_script_js)

        sleep(3)

