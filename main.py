# -*- coding: utf-8 -*-

# system


# project
from globals import Proxys
from globals import Invitation
from movie_inviter import MovieInviter


def main():
    # argparse that will get the details or interactively
    invitation = Invitation(site="https://globusmax.co.il/",
                            cinema_id=2, movie_id=1117, date="26/12/2018", time="13:20", lang="dub",
                            seats_places=
                            {
                                7: [7, 6, 5],
                                9: [1, 2, 3]
                            })

    # using the driver with random proxys
    proxy_address = Proxys.get_random_proxy()
    print "proxy: " + proxy_address
    movie_inviter = MovieInviter(proxy=None, display=True)
    movie_inviter.invite(invitation)


if __name__ == '__main__':
    main()
