# from fake_useragent import UserAgent
import inspect
import os
import re
import random
import time

import requests
import urllib
from urllib import request
from http import cookiejar
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
#跳过SSL验证证书
import ssl
#设置忽略SSL验证
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType

from config import phantomjs_driver, generate_cookie_url, chrome_driver, generate_cookie_url, cookie_max_num, \
    cookie_timeout, cookie_retry_num, cookie_interval_time, log_dir
from proxy_ip import _proxy

ssl._create_default_https_context = ssl._create_unverified_context
# ua = UserAgent()
is_clear = False

# 请求头设置
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
]

cookies_local = [
    # 'Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1570863645; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570863645; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201570863645213%2C%22updated%22%3A%201570863645213%2C%22info%22%3A%201570863645215%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; zg_did=%7B%22did%22%3A%20%2216dbec5021a4a-08c6a2d2b-212596f-1fa400-16dbec5021bc1%22%7D; CNZZDATA1254842228=442029587-1570858569-%7C1570858569; UM_distinctid=16dbec501f07d-04ce86a1b-212596f-1fa400-16dbec501f199; _uab_collina=157086364512186648153514; QCCSESSID=hmq62akb30eke67m1n2f278il4; acw_tc=3a31f82915708636456012732ecf3ba80b6185dee822061903f9e5b1da',
    # 'UM_distinctid=16d4d781a883e4-0d488cc5eb0bd7-3c375c0f-1fa400-16d4d781a897c2; zg_did=%7B%22did%22%3A%20%2216d4d781c73a19-0fb78f64911642-3c375c0f-1fa400-16d4d781c74a96%22%7D; acw_tc=b461944815692075174591116e8a95313d793072a098bc5d25603e8d1f; CNZZDATA1254842228=1131157379-1569203429-%7C1570764115; PHPSESSID=08nm7mpag75i4suu6vhjktjkr5; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570582899,1570669757,1570759579,1570768721; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201570768502820%2C%22updated%22%3A%201570768743947%2C%22info%22%3A%201570519912754%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%220096bdea6a9eec62a4a96030c7eee5f4%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1570768744',
    # 'UM_distinctid=16d4d781a883e4-0d488cc5eb0bd7-3c375c0f-1fa400-16d4d781a897c2; zg_did=%7B%22did%22%3A%20%2216d4d781c73a19-0fb78f64911642-3c375c0f-1fa400-16d4d781c74a96%22%7D; acw_tc=b461944815692075174591116e8a95313d793072a098bc5d25603e8d1f; CNZZDATA1254842228=1131157379-1569203429-%7C1570764115; PHPSESSID=08nm7mpag75i4suu6vhjktjkr5; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201570768502820%2C%22updated%22%3A%201570768721425%2C%22info%22%3A%201570519912754%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%220096bdea6a9eec62a4a96030c7eee5f4%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570582899,1570669757,1570759579,1570768721; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1570768721',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695379242%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695379',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695791508%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695792',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695924595%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695925',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535696003819%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535696005'
]


cookies_remote = [
    # 'UM_distinctid=16d4d781a883e4-0d488cc5eb0bd7-3c375c0f-1fa400-16d4d781a897c2; zg_did=%7B%22did%22%3A%20%2216d4d781c73a19-0fb78f64911642-3c375c0f-1fa400-16d4d781c74a96%22%7D; acw_tc=b461944815692075174591116e8a95313d793072a098bc5d25603e8d1f; PHPSESSID=kmkidh3g88g30g1pj9bl52fs72; CNZZDATA1254842228=1131157379-1569203429-%7C1571017916; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570759579,1570768721,1570846940,1571019811; acw_sc__v2=5da3e9a1be257a17025df93d9c9ec7d42083b644; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1571023271; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201571023266609%2C%22updated%22%3A%201571023271324%2C%22info%22%3A%201570519912754%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.qichacha.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%220096bdea6a9eec62a4a96030c7eee5f4%22%7D',
    # 'UM_distinctid=16d4d781a883e4-0d488cc5eb0bd7-3c375c0f-1fa400-16d4d781a897c2; zg_did=%7B%22did%22%3A%20%2216d4d781c73a19-0fb78f64911642-3c375c0f-1fa400-16d4d781c74a96%22%7D; acw_tc=b461944815692075174591116e8a95313d793072a098bc5d25603e8d1f; CNZZDATA1254842228=1131157379-1569203429-%7C1570764115; PHPSESSID=08nm7mpag75i4suu6vhjktjkr5; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570582899,1570669757,1570759579,1570768721; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201570768502820%2C%22updated%22%3A%201570768743947%2C%22info%22%3A%201570519912754%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%220096bdea6a9eec62a4a96030c7eee5f4%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1570768744',
    # 'UM_distinctid=16d4d781a883e4-0d488cc5eb0bd7-3c375c0f-1fa400-16d4d781a897c2; zg_did=%7B%22did%22%3A%20%2216d4d781c73a19-0fb78f64911642-3c375c0f-1fa400-16d4d781c74a96%22%7D; acw_tc=b461944815692075174591116e8a95313d793072a098bc5d25603e8d1f; CNZZDATA1254842228=1131157379-1569203429-%7C1570764115; PHPSESSID=08nm7mpag75i4suu6vhjktjkr5; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201570768502820%2C%22updated%22%3A%201570768721425%2C%22info%22%3A%201570519912754%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%220096bdea6a9eec62a4a96030c7eee5f4%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1570582899,1570669757,1570759579,1570768721; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1570768721',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695379242%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695379',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695791508%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695792',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535695924595%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535695925',
    # 'UM_distinctid=16518280d1e3e5-00788a93df88f7-5b193413-1fa400-16518280d1f949; zg_did=%7B%22did%22%3A%20%2216518280dd3b45-0da4e4ab13f793-5b193413-1fa400-16518280dd51f6%22%7D; acw_tc=7b81f49815356947470295339e1fc37a590000ea6190b3cf75ab42853b; PHPSESSID=4l787fmr2v90mh2khj8n6n64l5; CNZZDATA1254842228=226405416-1535690886-null%7C1535690886; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1535595956,1535618789,1535618810,1535694746; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201535694746927%2C%22updated%22%3A%201535696003819%2C%22info%22%3A%201535595953976%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.baidu.com%22%2C%22cuid%22%3A%20%227d775544e16a1cc0d0ab63b42b4b8aef%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1535696005'
]


def random_user_agent():
    # ua.random()
    return random.choice(user_agent)


def random_cookie():
    return random.choice(cookies_local)


def get_headers():
    return {
        # 'Host': 'm.qichacha.com',
        # 'Connection': 'keep-alive',
        # 'Accept': 'text/html, */*; q=0.01',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': random.choice(user_agent),
        'cookie': getGenerateCookie()
    }


def get_proxy_headers(proxy_ip):
    return {
        # 'Host': 'm.qichacha.com',
        # 'Connection': 'keep-alive',
        # 'Accept': 'text/html, */*; q=0.01',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': random.choice(user_agent),
        'cookie': generateProxyCookie(proxy_ip)
    }


# 获取cookie
def getGenerateCookie():
    cookie = None
    while True:
        if not is_clear and len(cookies_local) > 0:
            cookie = random.choice(cookies_local)
            break
        # elif is_clear:
            # print('is clearing...')
    return cookie


# 生成cookie
def generateCookie():
    if len(cookies_local) == cookie_max_num:
        # 在函数内部修改全局变量的值，要先用global声明全局变量。
        # print('to clear...')
        global is_clear
        is_clear = True
        cookies_local.clear()

    for i in range(cookie_max_num):
        for j in range(cookie_retry_num):
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
            desired_capabilities["phantomjs.page.settings.userAgent"] = (random.choice(user_agent))
            # 不载入图片，爬页面速度会快很多
            desired_capabilities["phantomjs.page.settings.loadImages"] = False

            # 创建一个参数对象,用来控制chrome以无界面打开
            # chrome_options = Options()
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--user-agent='+random.choice(user_agent))
            # chrome_options.add_argument('--headless')  # 开启无界面模式
            # chrome_options.add_argument('--disable-gpu')  # 禁用gpu，解决一些莫名的问题
            # chrome_options.add_argument('--no-sandbox')
            # driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)    # 此方法总是超时
            # driver = webdriver.Chrome(executable_path=chrome_driver)
            # driver.maximize_window()
            # driver.minimize_window()

            # PhantomJS创建无界面的浏览器对象
            # 获取当前文件路径
            current_path = inspect.getfile(inspect.currentframe())
            # 获取当前文件所在目录，相当于当前文件的父目录
            dir_name = os.path.dirname(current_path)
            # 转换为绝对路径
            file_abs_path = os.path.abspath(dir_name)
            driver = webdriver.PhantomJS(executable_path=file_abs_path+phantomjs_driver,
                                         service_log_path=file_abs_path+log_dir+r'\ghostdriver.log')
            driver.start_session(desired_capabilities)
            # 隐式等待5秒，可以自己调节
            driver.implicitly_wait(5)
            # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
            # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
            driver.set_page_load_timeout(cookie_timeout)
            # 设置10秒脚本超时时间
            driver.set_script_timeout(cookie_timeout)
            try:
                # print(generate_cookie_url)
                driver.get(generate_cookie_url)
                # 获取cookie列表
                cookie_list = driver.get_cookies()
                # print(cookie_list)
                # session_id
                # session_id = driver.session_id
                # html源码
                # page_source = driver.page_source
                cookie_lst = []
                # 格式化打印cookie
                for cookiee in cookie_list:
                    cookie_lst.append('{}={}'.format(cookiee['name'], cookiee['value']))
                cookie = "; ".join(cookie_lst)
                # print('cookie=============={}'.format(cookie))
                cookies_local.append(cookie)
                if is_clear:
                    is_clear = False
                break
            except NoSuchElementException as e:
                print('==============没有找到元素==============')
                print(str(e))
            except TimeoutException as e:
                print('==============生成cookie超时============')
                print(str(e))
                print('请求超时{}次，正在重新生成cookie......'.format(j+1))
            except Exception as e:
                print('==============生成cookie异常============')
                print(str(e))
                print('请求异常{}次，正在重新生成cookie......'.format(j+1))
            finally:
                driver.close()
                driver.quit()   # phantomJS进程需要关闭，不然在内存中驻留的phantomJS进程越来越多，最终吃光内存。
            time.sleep(random.randint(3, 10))  # 每隔3到10秒
    # print('cookie=============={}'.format(cookies_local))


# 使用代理生成cookie
def generateProxyCookie(proxy_ip):
    cookie = None
    if len(cookies_remote) > 0:
        return random.choice(cookies_remote)
    for i in range(cookie_retry_num):
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        desired_capabilities["phantomjs.page.settings.userAgent"] = (random.choice(user_agent))
        # 不载入图片，爬页面速度会快很多
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = getWebdriverProxy(proxy_ip)
        # 将代理设置添加到desired_capabilities中
        proxy.add_to_capabilities(desired_capabilities)
        driver = webdriver.PhantomJS(executable_path=phantomjs_driver)
        driver.start_session(desired_capabilities)
        # 隐式等待5秒，可以自己调节
        driver.implicitly_wait(5)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        driver.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        driver.set_script_timeout(10)
        try:
            # driver.get(generate_cookie_url)
            driver.get(generate_cookie_url)
            cookie_list = driver.get_cookies()
            # print(cookie_list)
            # session_id
            # session_id = driver.session_id
            # html源码
            # page_source = driver.page_source
            # print(page_source)
            cookie_lst = []
            # 格式化打印cookie
            for cookiee in cookie_list:
                cookie_lst.append('{}={}'.format(cookiee['name'], cookiee['value']))
            cookie = "; ".join(cookie_lst)
            cookies_remote.append(cookie)
            break
        except TimeoutException as e:
            print('==============使用代理生成cookie超时============')
            print(str(e))
            print('请求超时{}次，正在重新生成cookie......'.format(i+1))
            # cookie = random.choice(cookies_remote)
        except Exception as e:
            print('==============使用代理生成cookie异常============')
            print(str(e))
            print('请求异常{}次，正在重新生成cookie......'.format(i+1))
            # cookie = random.choice(cookies_remote)
        finally:
            driver.close()
            driver.quit()  # phantomJS进程需要关闭，不然在内存中驻留的phantomJS进程越来越多，最终吃光内存。
        time.sleep(random.randint(3, 10))  # 每隔3到10秒
    print('cookie=============={}'.format(cookie))
    return cookie


# 使用代理生成cookie
# 目前这个报错：selenium.common.exceptions.WebDriverException: Message: Can not connect to GhostDriver on port
def generateProxyCookie2(proxy_ip):
    # url = 'http://m.qichacha.com/user_login'
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    desired_capabilities["phantomjs.page.settings.userAgent"] = (random.choice(user_agent))
    # 不载入图片，爬页面速度会快很多
    desired_capabilities["phantomjs.page.settings.loadImages"] = False
    # proxyIp = '127.0.0.1:9999'
    proxyIp = getWebdriverProxy(proxy_ip)
    # 打开带配置信息的phantomJS浏览器
    service_args = [
        '--proxy={}'.format(proxyIp),         # 代理 IP：prot    （eg：192.168.0.28:808）
        '--proxy-type=socks5',            # 代理类型：http/https
        '--load - images = no',         # 关闭图片加载（可选）
        '--disk-cache=ye',              # 开启缓存（可选）
        '--ignore-ssl-errors=true'      # 忽略https错误（可选）
        ]
    driver = webdriver.PhantomJS(executable_path=phantomjs_driver,desired_capabilities=desired_capabilities,service_args=service_args)
    # 隐式等待5秒，可以自己调节
    driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(10)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(10)
    try:
        driver.get(generate_cookie_url)
        # 获取cookie列表
        cookie_list = driver.get_cookies()
        # print(cookie_list)
        # session_id
        # session_id = driver.session_id
        # html源码
        # page_source = driver.page_source
        cookie_lst = []
        # 格式化打印cookie
        for cookie in cookie_list:
            # print('Name = {}，Value = {}'.format(str(cookie['name']), str(cookie['value'])))
            cookie_lst.append('{}={}'.format(cookie['name'], cookie['value']))
        cookies = "; ".join(cookie_lst)
        # print(cookies)
        driver.quit()  # phantomJS进程需要关闭，不然在内存中驻留的phantomJS进程越来越多，最终吃光内存。
        return cookies
    except TimeoutException as e:
        driver.quit()  # phantomJS进程需要关闭，不然在内存中驻留的phantomJS进程越来越多，最终吃光内存。
        print('==============使用代理生成cookie连接超时============')
        print(str(e))
        return random.choice(cookies_local)
    except Exception as e:
        driver.quit()  # phantomJS进程需要关闭，不然在内存中驻留的phantomJS进程越来越多，最终吃光内存。
        print('==============使用代理生成cookie异常============')
        print(str(e))
        return random.choice(cookies_local)


def getWebdriverProxy(proxy_ip):
    for ip in proxy_ip.values():
        return ip.split('//')[1]


def getCookie():
    url = 'http://m.qichacha.com/user_login'
    Hostreferer = {
        #'Host':'***',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    #urllib或requests在打开https站点是会验证证书。 简单的处理办法是在get方法中加入verify参数，并设为False
    html = requests.get(url, headers=Hostreferer, verify=False)
    #获取cookie:DZSW_WSYYT_SESSIONID
    if html.status_code == 200:
        print(html)
        print(html.cookies)
        for cookie in html.cookies:
            print(cookie)


def getCookie2():
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    url = 'http://m.qichacha.com/user_login'
    response = opener.open(url)
    # 打印cookie信息
    for item in cookie:
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)


if __name__ == '__main__':
    # getCookie()
    # getCookie2()
    for i in range(100):
        generateCookie()
    # generateProxyCookie(_proxy())
    # print('等待一分钟...')
    # time.sleep(60)
    # interval_time = time.time() - start_time
    # print(interval_time//60)
