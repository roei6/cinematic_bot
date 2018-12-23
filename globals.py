import random

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

