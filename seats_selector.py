# system
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver


class SeatsSelector(object):
    def __init__(self, driver):
        self.driver = driver
        assert (isinstance(driver, WebDriver))

    def save_seats(self, seats_places):
        assert(isinstance(seats_places, dict))

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "ddQunatity_0"))
        )

        self.select_stuff("ddQunatity_0", str(sum(len(i) for i in seats_places.values())))

        elem = self.driver.find_element_by_id('lbSelectSeats')
        elem.click()
        sleep(3)
        for line in seats_places.keys():
            self.click_on_seats(line, seats_places[line])

        while True:
            sleep(3)
            elem = self.driver.find_element_by_id('btnNext')
            elem.click()
            sleep(60 * 6.5)
            print "refreshing"
            elem = self.driver.find_element_by_id('ctl00_CPH1_lbBackButton_hlBack')
            elem.click()

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

    def select_stuff(self, attribute, value):
        select_script_js = """
                const change_ev = new Event("change");
                const {attribute}_name = document.querySelector('#{attribute}');
                {attribute}_name.value = "{value}";
                {attribute}_name.dispatchEvent(change_ev);
                """.format(attribute=attribute, value=value)
        self.driver.execute_script(select_script_js)

