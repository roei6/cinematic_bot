# system
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# project
from proxys_race import ProxysRace
from seats_selector import SeatsSelector
from netmotorist import NetMotorist, UnexpectedPage


class MovieInviter(object):
    def __init__(self, proxy=None, display=False, enable_adblock=False):
        self.driver = ProxysRace().get_fastest(display, enable_adblock)
        self.driver.implicitly_wait(30)

    def __del__(self):
        self.driver.close()

    def invite(self, invitation):
        # globusmax:
        self.driver.get(invitation.site)
        self.driver.refresh_loop("-", 5, 3)
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

        print "selecting the movie stuff"

        self.driver.select_stuff("cinema", invitation.cinema_id)
        self.driver.select_stuff("movie", invitation.movie_id)
        self.driver.select_stuff("lang", invitation.lang)
        self.driver.select_stuff("date", invitation.date)
        self.driver.select_stuff("time", invitation.time)

        sleep(5)

        url = self.driver.current_url

        # click on the invite button # should be done in js
        elem = self.driver.find_element_by_class_name('send_btn')
        elem.click()

        if url == self.driver.current_url:
            raise UnexpectedPage

        print "selecting tickets"

        seats_selector = SeatsSelector(self.driver)
        seats_selector.save_seats(invitation.seats_places)
        # seats selector:





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
