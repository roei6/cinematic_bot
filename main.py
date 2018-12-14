# system
from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# project
from globals import Proxys


def main():
    # using the driver with random proxys
    proxy_address = Proxys.get_random_proxy()
    print "proxy: " + proxy_address
    start_driver(proxy=proxy_address, display=True)


def start_driver(proxy=None, display=False, enable_adblock=False):
    """
    starts the driver with the requested setting
    :param proxy: the proxy desired to use the driver, if not given then there will no use in proxy server
    :param display: determine whether to show the driver or not
    :param enable_adblock: do you need adblock or not?
    :return: the time the whole driver took
    """

    chrome_options = get_options(proxy, display, enable_adblock)

    start_time = time()
    with webdriver.Chrome(chrome_options=chrome_options) as driver:
        driver.get("https://globusmax.co.il/movie-1246-spider_man_into_the_spiderverse")
        refresh_loop(":", driver, 5, 3)
        print "done loading the page"
        elem = driver.find_element_by_xpath('//div[@data-eventid="59503"]')
        elem.click()
        print "it worked"
        sleep(15)
    end_time = time()
    return (end_time - start_time)


def refresh_loop(part_of_title, driver, timeout, max_tries):
    """
    refreshes the driver until it in the right place or timeout
    :param driver:
    :return:
    """
    tries_count = 0
    while part_of_title not in driver.title:
        sleep(timeout)
        driver.refresh()
        tries_count += 1
        if tries_count >= max_tries:
            raise Exception


def get_options(proxy, display, enable_adblock):
    chrome_options = Options()
    # disable showing the driver
    if not display:
        chrome_options.add_argument("--headless")
        # don't load photos
        prefs = {'profile.default_content_setting_values': {'images': 2,
                                                            'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                            'notifications': 2, 'auto_select_certificate': 2,
                                                            'fullscreen': 2,
                                                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                            'media_stream_mic': 2, 'media_stream_camera': 2,
                                                            'protocol_handlers': 2,
                                                            'ppapi_broker': 2, 'automatic_downloads': 2,
                                                            'midi_sysex': 2,
                                                            'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                            'metro_switch_to_desktop': 2,
                                                            'protected_media_identifier': 2, 'app_banner': 2,
                                                            'site_engagement': 2,
                                                            'durable_storage': 2}}
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


if __name__ == '__main__':
    main()
