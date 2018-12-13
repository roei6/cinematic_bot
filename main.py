# system
from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# project
from globals import Proxys

on_background = False
on_vpn = True

def main():
    chrome_options = Options()
    # disable showing the driver
    if on_background:
        chrome_options.add_argument("--headless")

    if on_vpn:
        proxy_addr = Proxys.get_random_proxy()
        print "proxy: "+ proxy_addr
        chrome_options.add_argument("--proxy-server={proxy}".format(proxy=proxy_addr))
    else:
        chrome_options.add_argument("--no-proxy-server")
        chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--proxy-server='direct://'")

    # adblock:
    # chrome_options.add_extension(
    #     r"C:\Users\roei\AppData\Local\Google\Chrome\User Data\Default\Extensions\gighmmpiobklfepjocnamgkkbiglidom")

    print "starting..."
    start_time = time()
    with webdriver.Chrome(chrome_options=chrome_options) as driver:
        print "driver is open"
        driver.get("https://whoer.net/#extended")
        print driver.title
        assert "IP" in driver.title
        elem = driver.find_element_by_class_name("your-ip")
        print "your ip is now: " + elem.text
        sleep(10)
    end_time = time()
    print "finished with time: " + str(end_time - start_time)


if __name__ == '__main__':
    main()
