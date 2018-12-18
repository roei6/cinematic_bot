# -*- coding: utf-8 -*-

# system
from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# project
from globals import Proxys


def main():
    # using the driver with random proxys
    proxy_address = Proxys.get_random_proxy()
    print "proxy: " + proxy_address
    start_driver(proxy=None, display=True)


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
        driver.get("https://globusmax.co.il/")
        refresh_loop("-", driver, 5, 3)
        print "done loading the page"

        # try to close the advertisement
        try:
            elem = driver.find_element_by_id('ZA_CANVAS_436229_CLOSE_IMG2_8_IMG')
            elem.click()
            print "ad closed"
        except Exception:
            print "could not load ad"

        # wait for the ad to disappear
        sleep(2)

        select_stuff(driver, "cinema", "5")
        select_stuff(driver, "movie", "1246")
        select_stuff(driver, "lang", "dub")
        select_stuff(driver, "date", "20/12/2018")
        select_stuff(driver, "time", "16:50")


        # click on the invite button
        elem = driver.find_element_by_class_name('send_btn')
        elem.click()


        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ddQunatity_0"))
        )


        select_stuff(driver, "ddQunatity_0", "1")

        elem = driver.find_element_by_id('lbSelectSeats')
        elem.click()

        sleep(3)

        canvas = driver.find_element_by_id("myCanvas")
        drawing = ActionChains(driver) \
            .move_to_element(canvas)  \
            .move_by_offset(-33, 33) \
            .click()
        drawing.perform()


        print "it worked"
        sleep(120)
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
    # prefs = {'profile.default_content_setting_values': {'images': 2}}
    # chrome_options.add_experimental_option("prefs", prefs)

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


def select_stuff(driver, attribute, value):
    select_script_js = """
            const change_ev = new Event("change");
            const {attribute}_name = document.querySelector('#{attribute}');
            {attribute}_name.value = "{value}";
            {attribute}_name.dispatchEvent(change_ev);
            """.format(attribute=attribute, value=value)
    driver.execute_script(select_script_js)

    sleep(2)


if __name__ == '__main__':
    main()
