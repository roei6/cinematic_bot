from time import sleep

from selenium.webdriver.chrome.options import Options
import threading

from globals import Proxys
from netmotorist import NetMotorist, NoInternetPageException, UnexpectedPage

lock = threading.Lock()


class ProxysRace(object):
    def __init__(self):
        self.failed_proxys = []
        self.current_failed_proxys = []
        self.first_proxy = None
        self.driver = None

    def win_race(self, proxy, driver):
        with lock:
            if not self.winner_exists():
                self.first_proxy = proxy
                self.driver = driver
                return True
            else:
                print "i am late"
                return False

    def get_fastest(self, display=False, enable_adblock=False, number_of_proxys=3, avoid=None):
        if avoid is None:
            avoid = []

        while True:
            actual_number_of_proxys = self.start_race(display, enable_adblock, number_of_proxys,
                                                      avoid + self.failed_proxys)
            winning_driver = self.check_winner(actual_number_of_proxys)
            if winning_driver is not None:
                return winning_driver

    def start_race(self, display, enable_adblock, number_of_proxys, avoid):
        proxy_list = Proxys.get_multiple_random_proxys(num=number_of_proxys, avoid=avoid)

        print "testing proxys: {proxys}".format(proxys=proxy_list)

        if len(proxy_list) == 0:
            raise IndexError

        # start all given proxys in different threads
        for proxy in proxy_list:
            thread = threading.Thread(target=self.challenge_func, args=(proxy, display, enable_adblock))
            thread.start()

        return len(proxy_list)

    def check_winner(self, number_of_proxys):
        # constantly check the values
        while True:
            with lock:
                if self.winner_exists():
                    # WE HAVE A WINNER
                    print "{proxy} finished loading!".format(proxy=self.first_proxy)
                    return self.driver
                elif len(self.current_failed_proxys) == number_of_proxys:
                    self.failed_proxys += self.current_failed_proxys
                    self.current_failed_proxys = []
                    print "y'all suck I want other proxys"
                    # all the given proxys has failed.. we need to try to get new proxys
                    return None
            sleep(0.5)

    def challenge_func(self, proxy, display, enable_adblock):
        driver = NetMotorist(chrome_options=self.__get_options(proxy, display, enable_adblock))
        driver.get("https://globusmax.co.il/")
        try:
            self.refresh_loop(driver, "-", 5, 3)
        except Exception:
            self.current_failed_proxys.append(proxy)
            print "i am a failure"
            driver.quit()
            return

        if not self.win_race(proxy, driver):
            print "well, not my day"
            driver.quit()
        else:
            print "i won bitches"

    def refresh_loop(self, driver, part_of_title, timeout=3, max_tries=3, no_internet_quit=True):
        """
        refreshes the driver until it in the right place or timeout

        :param no_internet_quit: quit when there is no internet exception
        :param max_tries: max tries
        :param timeout: the timeout between every refresh
        :param part_of_title: part of the title that is desired
        :return:
        """
        tries_count = 0
        while part_of_title not in driver.title:
            sleep(timeout)
            if self.winner_exists():
                raise Exception
            driver.refresh()
            tries_count += 1
            if tries_count >= max_tries:
                if (driver.on_no_internet_page()):
                    if no_internet_quit:
                        driver.quit()
                    raise NoInternetPageException
                else:
                    raise UnexpectedPage

    @staticmethod
    def __get_options(proxy, display, enable_adblock):
        chrome_options = Options()
        # disable showing the driver
        if not display:
            chrome_options.add_argument("--headless")
            # don't load photos
        prefs = {'profile.default_content_setting_values': {'images': 2}}
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

    def winner_exists(self):
        return self.first_proxy is not None and self.driver is not None
