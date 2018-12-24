# system
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# project
from seats_selector import SeatsSelector

class MovieInviter(object):
    def __init__(self, proxy=None, display=False, enable_adblock=False):
        self.driver = webdriver.Chrome(chrome_options=self.__get_options(proxy, display, enable_adblock))

    def __del__(self):
        self.driver.close()

    def invite(self, invitation):
        # globusmax:
        self.driver.get(invitation.site)
        self.refresh_loop("-", 5, 3)
        print "done loading the page"

        sleep(1)

        # try to close the advertisement
        try:
            elem = self.driver.find_element_by_id('ZA_CANVAS_436229_CLOSE_IMG2_8_IMG')
            elem.click()
            print "ad closed"
            sleep(1)
        except Exception:
            print "could not load ad"

        self.select_stuff("cinema", invitation.cinema_id)
        self.select_stuff("movie", invitation.movie_id)
        self.select_stuff("lang", invitation.lang)
        self.select_stuff("date", invitation.date)
        self.select_stuff("time", invitation.time)

        sleep(5)

        # click on the invite button
        elem = self.driver.find_element_by_class_name('send_btn')
        elem.click()

        seats_selector = SeatsSelector(self.driver)
        seats_selector.save_seats(invitation.seats_places)
        # seats selector:

    def refresh_loop(self, part_of_title, timeout, max_tries):
        """
        refreshes the driver until it in the right place or timeout
        :param driver:
        :return:
        """
        tries_count = 0
        while part_of_title not in self.driver.title:
            sleep(timeout)
            self.driver.refresh()
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
        self.driver.execute_script(select_script_js)

        sleep(3)

    @staticmethod
    def __get_options(proxy, display, enable_adblock):
        chrome_options = Options()
        # disable showing the driver
        if not display:
            chrome_options.add_argument("--headless")
            # don't load photos
        # prefs = {'profile.default_content_setting_values': {'images': 2}}
        prefs = {'profile.default_content_setting_values': {"popups": 2}}
        chrome_options.add_experimental_option("prefs", prefs)

        # setting a proxy to the given argument, if not then don't use proxy
        if proxy is not None:
            chrome_options.add_argument("--proxy-server={proxy}".format(proxy=proxy))
        else:
            chrome_options.add_argument("--no-proxy-server")
            chrome_options.add_argument("--proxy-bypass-list=*")
            chrome_options.add_argument("--proxy-server='direct://'")

        if enable_adblock:
            chrome_options.add_argument(
                r"load-extension=C:\Users\roei\PycharmProjects\cinematic_bot\extentions\adblock")

        return chrome_options


# def canvas_click(driver, canvas, x, y):
#     try:
#         x *= 32
#         x -= 323
#         y *= 32
#         y -= 132
#         clicking = ActionChains(driver) \
#             .move_to_element(canvas) \
#             .move_by_offset(x, y) \
#             .click()
#         clicking.perform()
#         print "clicked on {x},{y}".format(x=x, y=y)
#     except UnexpectedAlertPresentException:
#         alert = driver.switch_to.alert
#         alert.accept()
