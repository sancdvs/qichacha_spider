import re
import urllib

import requests
import json
import random

from config import proxy_ip_url

# url = 'http://127.0.0.1:8111/proxy?count=10'
# url = 'http://127.0.0.1:8111/proxy?count=10&anonymity=anonymous'
# 这边需要本地部署一个提供代理IP的应用，这里使用的是proxy_list-master

def _proxy():
    """
    获取一个已爬代理
    :return:
    """
    response = requests.get(proxy_ip_url, **{'timeout': 5})
    text = response.text
    proxyy = json.loads(text)
    proxy = random.choice(proxyy)   # 从10个中随机取一个
    # print(proxyy)
    # print(proxy)
    return {proxy[0]: "{}://{}:{}".format(proxy[0], proxy[1], proxy[2])}
    # return {proxy[0]: "{}:{}".format(proxy[1], proxy[2])}
    # return {'http': "http://{}:{}".format(proxy[1], proxy[2]),
    #         'https': "http://{}:{}".format(proxy[1], proxy[2])}


def is_internet():
    try:
        url = "https://www.baidu.com"
        html = requests.get(url)
        if html.status_code == 200:
            return True
        else:
            return False
    except ConnectionError:
        return False


if __name__ == '__main__':
    # _proxy()
    print(is_internet())