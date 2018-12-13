import random

# servers took from: https://free-proxy-list.net/

proxys_list = \
    [
        # "114.34.168.157:46160",  # captcha required
        # "178.136.11.7:48816",    # suspicious ip
        # "159.65.105.99:3128",    # proxy detected
        # "167.99.73.246:3128",    # proxy detected
        # "209.97.163.194:8080",   # proxy detected
        # "65.152.237.149:53281",  # proxy detected
        # "149.56.129.139:8888",   # proxy detected
        # "45.32.190.16:3128",     # proxy detected
        "176.37.46.44:56144",      # perfect
        "97.68.17.66:53281",       # perfect
        "190.220.255.115:61376"    # perfect
    ]

class Proxys(object):
    @staticmethod
    def get_random_proxy():
        return random.choice(proxys_list)
