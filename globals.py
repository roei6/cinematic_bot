import random

proxys_list = \
    [
        "97.68.17.66:53281",
        "136.25.2.43:33773",
        "65.152.237.149:53281",
        "159.65.105.99:3128",
        "176.37.46.44:56144",
        "178.136.11.7:48816",
        "190.220.255.115:61376",
        "46.63.162.171:8080",
    ]


class Proxys(object):
    @staticmethod
    def get_random_proxy():
        return random.choice(proxys_list)
