# -*- coding: utf-8 -*-

# system
import logging
import traceback
from selenium.common.exceptions import TimeoutException

# project
from globals import Proxys
from globals import Invitation
from insomniac import Insomniac
from movie_inviter import MovieInviter
from netmotorist import NoInternetPageException


def main():
    logging.error("creating logger")
    # argparse that will get the details or interactively
    invitation = Invitation(site="https://globusmax.co.il/",
                            cinema_id=14, movie_id=1294, date="28/12/2018", time="00:00", lang="sub",
                            seats_places=
                            {
                                9: [10, 11],
                            })

    # make sure the computer stays awake
    with Insomniac():
        # using the driver with random proxys
        if not invite_with_proxys(invitation):
            exit(1)


def invite_with_proxys(invitation):
    avoid_proxys_list = []  # this list will hold the current proxys that don't work and we don't want to get
    proxy_address = ""
    while True:
        try:
            proxy_address = Proxys.get_random_proxy(avoid=avoid_proxys_list)
            print "proxy: " + proxy_address
            movie_inviter = MovieInviter(proxy=proxy_address, display=True)
            movie_inviter.invite(invitation)
            break
        except (NoInternetPageException, TimeoutException):
            # there is probably no internet on this proxy right now, we need to use another one
            print "removing {proxy} for this invitation".format(proxy=proxy_address)
            avoid_proxys_list.append(proxy_address)
            pass
        except IndexError:
            # we will get to this exception if random.choice got an empty list
            print "could not complete request, all proxys failed. please check your internet connection"
            return False
        except KeyboardInterrupt:
            print "keyboard interrupt"
            return True
        except BaseException as e:
            print "Unknown execption"
            logging.getLogger('unknownErrors').error(e.message + ": " + traceback.format_exc())


if __name__ == '__main__':
    main()
