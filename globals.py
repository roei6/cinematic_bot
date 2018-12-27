import random


class Invitation(object):
    """
    contains all the invitation information for ordering the movie,
    """
    def __init__(self, site, cinema_id, movie_id, date, time, seats_places, movie_type="normal", lang="sub"):
        """
        :type site: str
        :type cinema_id: int
        :type movie_id: int
        :type date: str
        :type time: str
        :type seats_places: dict
        :type movie_type: str
        :type lang: str
        """
        self.site = site
        self.cinema_id = cinema_id
        self.movie_id = movie_id
        self.date = date
        self.time = time
        self.lang = lang
        self.movie_type = movie_type
        self.seats_places = seats_places


class Proxys(object):
    # servers took from: https://free-proxy-list.net/
    proxys_list = \
        [
            "176.37.46.44:56144",
            "97.68.17.66:53281",
            # "195.189.89.122:32193",  # ?
            "190.210.245.200:60539",
            "185.31.163.21:35786",
            "78.36.202.254:32337",
            "150.242.109.121:53153",
            "1.20.101.95:49062",
            # "190.220.255.115:61376"  # ?
        ]

    @staticmethod
    def get_random_proxy():
        return random.choice(Proxys.proxys_list)
