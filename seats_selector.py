# system
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# project
from netmotorist import NetMotorist


class SeatsSelector(object):
    """
    This object is used to select the seats from the SelectSeats site and save them
    """
    def __init__(self, driver):
        self.driver = driver
        assert (isinstance(driver, NetMotorist))

    def save_seats(self, seats_places):
        assert(isinstance(seats_places, dict))

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "ddQunatity_0"))
        )

        self.driver.select_stuff("ddQunatity_0", str(sum(len(i) for i in seats_places.values())))

        elem = self.driver.find_element_by_id('lbSelectSeats')
        elem.click()
        sleep(3)

        self.click_on_seats_places(seats_places)
        self.reordering_loop()

    def reordering_loop(self):
        while True:
            sleep(3)
            elem = self.driver.find_element_by_id('btnNext')
            elem.click()
            sleep(60 * 6.5)
            print "refreshing"
            elem = self.driver.find_element_by_id('ctl00_CPH1_lbBackButton_hlBack')
            elem.click()

    def click_on_seats_places(self, seats_places):
        for line in seats_places.keys():
            self.click_on_seats(line, seats_places[line])

    def click_on_seats(self, line, seats):
        for seat in seats:
            self.click_on_seat(line, seat)

    def click_on_seat(self, line, seat):
        # click on the selected seat
        print "clicking seat {seat} line {line}".format(seat=seat, line=line)
        select_script_js = """
                            var line = document.querySelectorAll('[id^="s_"][id$="_{line}"]');
                            for (var i = 0; i<line.length; i++)
                            {{
                                if (line[i].text == {seat}) line[i].click();
                            }}
                            """.format(line=line, seat=seat)
        self.driver.execute_script(select_script_js)
        sleep(.1)


