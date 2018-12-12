# system
from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# project
from globals import Proxys

on_background = True
on_vpn = True

def main():
    chrome_options = Options()
    # disable showing the driver
    if on_background:
        chrome_options.add_argument("--headless")

    if on_vpn:
        chrome_options.add_argument("--proxy-server={proxy}".format(proxy=Proxys.get_random_proxy()))
    else:
        chrome_options.add_argument("--no-proxy-server")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--proxy-server='direct://'")

    print "starting..."
    start_time = time()
    with webdriver.Chrome(options=chrome_options) as driver:
        print "driver is open"
        driver.get("http://www.whatsmyip.org/")
        print driver.title
        assert "IP" in driver.title
        elem = driver.find_element_by_id("ip")
        print "your ip is now: " + elem.text
    end_time = time()
    print "finished with time: " + str(end_time - start_time)


if __name__ == '__main__':
    main()
