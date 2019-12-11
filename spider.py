# encoding:utf-8
# requests库用于爬取HTML页面，提交网络抓取
import inspect
import os

import openpyxl
import requests
# xlwt模块针对Excel文件的创建、设置、保存
import xlrd
import xlwt
# 正则表达式模块
import re
import time
import random

from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from xlutils.copy import copy

from basic_info import export_basic_inf
from config import base_url, base_url1, enterprise_search_file, spider_timeout, spider_retry_num, cookie_interval_time, \
    spider_result_file_name, crawl_interval_mintime, crawl_interval_maxtime, chrome_driver, basic_inf_sheet_name, \
    partners_sheet_name, key_personnel_sheet_name, error_data_sheet_name, phantomjs_driver, log_dir
from error_data import export_error_data
from excel_util import check_file, check_sheet_exsit
from proxy_ip import _proxy, is_internet
from headers import get_headers, get_proxy_headers, generateCookie, cookies_local, random_user_agent, getChromeProxyIp, \
    random_cookie
from partners import export_partners
from key_personnel import export_key_personnel
from tools.myTimer import MyTimer
from log import logging

'''使用selenium爬取'''
def selenium_crawl(url,isProxy):
    # 获取当前文件路径
    current_path = inspect.getfile(inspect.currentframe())
    # 获取当前文件所在目录，相当于当前文件的父目录
    dir_name = os.path.dirname(current_path)
    # 转换为绝对路径
    file_abs_path = os.path.abspath(dir_name)
    '''
       这边报错Message: invalid cookie domain
       (Session info: headless chrome=77.0.3865.120)
       (Driver info: chromedriver=77.0.3865.40 (f484704e052e0b556f8030b65b953dce96503217-refs/branch-heads/3865@{#442}),platform=Windows NT 6.1.7601 SP1 x86_64)
       是由于Chrome驱动版本与本地浏览器的版本不一致所致，但是现在Chrome驱动还没有与之匹配的版本。
    '''
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--user-agent='+random_user_agent())
    # chrome_options.add_argument('--headless')  # 开启无界面模式
    # chrome_options.add_argument('--disable-gpu')  # 禁用gpu，解决一些莫名的问题
    # # chrome_options.add_argument('--no-sandbox')
    # if isProxy:
    #     # 设置代理
    #     proxy_ip = _proxy()
    #     chrome_options.add_argument("--proxy-server="+getChromeProxyIp(proxy_ip))
    # driver = webdriver.Chrome(executable_path=file_abs_path+chrome_driver, chrome_options=chrome_options)
    # driver.maximize_window()

    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    desired_capabilities["phantomjs.page.settings.userAgent"] = random_user_agent()
    # 不载入图片，爬页面速度会快很多
    desired_capabilities["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(executable_path=file_abs_path + phantomjs_driver,
                                 service_log_path=file_abs_path + log_dir + r'\ghostdriver.log')
    driver.start_session(desired_capabilities)

    # 隐式等待5秒，可以自己调节
    driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(spider_timeout)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(spider_timeout)
    driver.get(url)
    driver.delete_all_cookies()
    # 添加cookie
    cookies = get_cookie_dict(random_cookie())
    for name, value in cookies.items():
        cookie_dict = {
            "domain": ".qichacha.com",  # 火狐浏览器不用填写，谷歌要需要
            'name': name,
            'value': value,
            "expires": "",
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False}
        driver.add_cookie(cookie_dict=cookie_dict)
    # print(driver.page_source)
    return driver.page_source

def get_cookie_dict(cookie):
    cookie_dict = {}
    cookie_array = cookie.split('; ')
    for cook in cookie_array:
        cookie_dict[cook.split('=')[0]] = cook.split('=')[1]
    return cookie_dict

def export_excel(data, error_data):
    if check_file(spider_result_file_name):
        # 读取文件的时候需要将formatting_info参数设置为True，默认是False；保留样式，不然获取合并的单元格数组为空
        old_workbook = xlrd.open_workbook(spider_result_file_name, formatting_info=True)
        workbook = copy(old_workbook)  # 拷贝一份原来的excel
    else:
        # 创建输出excel文件
        workbook = xlwt.Workbook(encoding="utf-8")
    # 导出企业基本信息
    if len(data) > 0:
        print("==============================企业基本信息==============================")
        try:
            export_basic_inf(data, workbook, check_sheet_exsit(spider_result_file_name, basic_inf_sheet_name))
        except Exception as e:
            logging.error('===================写入企业基本信息异常===================')
            # logging.exception(e)
            logging.error(e)
        # 导出企业股东信息
        print("==============================企业股东信息==============================")
        try:
            export_partners(data, workbook, check_sheet_exsit(spider_result_file_name, partners_sheet_name))
        except Exception as e:
            logging.error('===================写入企业股东信息异常===================')
            # logging.exception(e)
            logging.error(e)
        # 导出企业主要人员s
        print("==============================企业主要人员==============================")
        try:
            export_key_personnel(data, workbook, check_sheet_exsit(spider_result_file_name, key_personnel_sheet_name))
        except Exception as e:
            logging.error('===================写入企业主要人员异常===================')
            # logging.exception(e)
            logging.error(e)
    # 导出抓取失败企业名称
    if len(error_data) > 0:
        print("==============================写入抓取失败企业==============================")
        try:
            export_error_data(error_data, workbook, check_sheet_exsit(spider_result_file_name, error_data_sheet_name))
        except Exception as e:
            logging.error('===================写入抓取失败企业异常===================')
            logging.error(e)
            # logging.exception(e)
    workbook.save(spider_result_file_name)


def verify(url):
    # url1 = 'https://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E5%90%88%E8%82%A5%E6%99%AF%E5%96%9C%E7%94%B5%E6%B0%94%E8%AE%BE%E5%A4%87%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8'
    # 创建一个参数对象,用来控制chrome以无界面打开
    # 获取当前文件路径
    current_path = inspect.getfile(inspect.currentframe())
    # 获取当前文件所在目录，相当于当前文件的父目录
    dir_name = os.path.dirname(current_path)
    # 转换为绝对路径
    file_abs_path = os.path.abspath(dir_name)
    driver = webdriver.Chrome(executable_path=file_abs_path+chrome_driver)
    driver.maximize_window()
    # 隐式等待5秒，可以自己调节
    driver.implicitly_wait(5)
    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(10)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(10)
    driver.get(url)

# 爬取目标页面重试
def retry_crawl(url, isProxy):
    response = None
    logging.error('抓取异常！正在试图重新抓取页面{}'.format(url))
    for i in range(spider_retry_num):
        logging.error('重新抓取第{}次'.format(i + 1))
        try:
            if isProxy:
                proxy = _proxy()
                print('正在使用代理{}，抓取页面 {}'.format(proxy, url))
                response = requests.get(url, headers=get_proxy_headers(proxy), proxies=proxy, timeout=spider_timeout)
            else:
                response = requests.get(url, headers=get_headers(), timeout=spider_timeout)
        except requests.exceptions.ProxyError as e:
            # logging.exception(e)
            logging.error(e)
            continue
        except requests.exceptions.ConnectTimeout as e:
            # logging.exception(e)
            logging.error(e)
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        com_all_info = soup.find_all(class_='m_srchList')
        _response = response.text
        if len(com_all_info) > 0:
            break
        # elif '<script>window.location.href=' in _response:  # 操作频繁验证链接
        #     verify_url = re.findall("<script>window.location.href='(.*?)';</script>", _response)[0]
        #     print('由于操作频繁被企查查识别为爬虫，请手动点击此链接验证：{}'.format(verify_url))
        #     # verify(verify_url)
        #     time.sleep(20)
        else:
            logging.error('=================返回异常=================')
            # logging.error(response.text)
        time.sleep(random.randint(crawl_interval_mintime, crawl_interval_maxtime))
    return response


# 去除重复的名称
def remove_repeat(list):
    list2 = []
    for i in list:
        name = i.replace('\n', '').replace(" ", "").replace('“', '').replace('”', '')\
            .replace('"', '').replace(')','）').replace( '(', '（').strip()
        if '' != name and not name.isspace() and name not in list2:
            list2.append(name)
        elif '' != name and not name.isspace():
            print('存在重复企业名称==========={}'.format(name))
    # print(list2)
    return list2


# 获取企业筛选信息链接
def get_detail_url(start_url, response,is_proxy):
    search_url = None
    soup = BeautifulSoup(response.text, 'lxml')
    com_all_info = soup.find_all(class_='m_srchList')
    if len(com_all_info) > 0:
        search_url = com_all_info[0].tbody.select('tr')[0].select('td')[2].select('a')[0].get('href')  # 取第一条数据
    elif len(soup.find_all(class_='noresult')) > 0:
        raise RuntimeError('没有找到该企业！')
    else:
        _response = retry_crawl(start_url, is_proxy)
        if _response is not None:
            _soup = BeautifulSoup(_response.text, 'lxml')
            _com_all_info = _soup.find_all(class_='m_srchList')
            if len(_com_all_info) > 0:
                search_url = _com_all_info[0].tbody.select('tr')[0].select('td')[2].select('a')[0].get('href')  # 取第一条数据
    print("获取筛选信息链接=============={}".format(search_url))
    return search_url


def readCookie():
    print('正在读取cookie......')
    f = open('cookie.txt', encoding='utf-8')
    cookies = f.readlines()
    for cookie in cookies:
        cookie = cookie.replace('\n', '').strip()
        cookies_local.append(cookie)
    if len(cookies_local) > 0:
        print('读取到cookie=============={}个'.format(len(cookies_local)))
    else:
        print('请保存登录企查查的cookie到cookie.txt文件中！')
        return


if __name__ == '__main__':
    print('>>>>>>>>>>>>>>>>>>>启动企查查爬虫程序>>>>>>>>>>>>>>>>>>>')
    print('********************************************************')
    print('本程序运行条件：')
    print('1、请先确保本程序处于外网环境！')
    print('2、为防止企查查网站反爬，每次程序运行间隔不少于30分钟！')
    print('3、一次爬取企业数量建议不大于100条！')
    print('4、程序执行过程中请勿关闭！')
    print('********************************************************')

    if is_internet():
        # 启动生成cookie定时任务
        # timer = MyTimer('生成cookie', cookie_interval_time, generateCookie)
        # timer.setDaemon(True)  # 设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行
        # timer.start()

        is_ok = input("请确认企业名称是否规范y/n？：")
        if 'y' == is_ok.lower():
            is_proxy = 'n'
            # is_proxy = input("是否启用ip代理y/n？：")
            is_proxy = True if is_proxy == 'y' else False
            readCookie()    # 从文件中读取cookie
            # 打开企业搜索文件
            f = open(enterprise_search_file, encoding='utf-8')
            enterprise_list = f.readlines()
            print('开始对文件进行重复检查......')
            _enterprise_list = remove_repeat(enterprise_list)
            print('去除重复后企业总数============={}'.format(len(_enterprise_list)))
            f.close()
            # 增加重试连接次数
            requests.adapters.DEFAULT_RETRIES = 5
            # 关闭多余的连接
            s = requests.session()
            s.keep_alive = False
            i = 0
            for name in _enterprise_list:
                if is_proxy:
                    try:
                        _proxy()
                    except Exception as e:
                        print('========================请先启动ip代理程序=======================')
                        break
                # 定义查询结果集
                data_list = []
                # 定义查询结果异常集
                error_data_list = []
                i += 1
                start_url = base_url + str(name)
                # print(start_url)
                try:
                    print("正在抓取第{}个公司==========================={}".format(i, name))
                    if is_proxy:
                        proxy = _proxy()
                        print('正在使用代理{}，抓取页面 {}'.format(proxy, start_url))
                        try:
                            response = requests.get(start_url, headers=get_proxy_headers(proxy), proxies=proxy, timeout=spider_timeout)
                        except Exception as e:
                            response = retry_crawl(start_url, is_proxy)
                    else:
                        try:
                            response = requests.get(start_url, headers=get_headers(), timeout=spider_timeout)
                        except Exception as e:
                            response = retry_crawl(start_url, is_proxy)
                    # if response.status_code != 200:
                    #     error_data_list.append(name)
                    #     print("抓取页面 {}，异常 {} 可能被企查查网站反爬拦截了！".format(start_url, response.status_code))
                    #     continue

                    # 获取企业筛选信息链接
                    if response is not None:
                        search_url = get_detail_url(start_url, response, is_proxy)
                        if search_url is None:
                            # print('请求企查查网站操作频繁，被反爬拦截了，需等待一段时间再试！')
                            # error_data_list.append(name)
                            # break
                            raise RuntimeError('请求企查查网站操作频繁，被反爬拦截了，需等待一段时间再试！')
                    url = base_url1 + search_url

                    time.sleep(random.randint(crawl_interval_mintime, crawl_interval_maxtime))  # 间隔一段时间

                    # if is_proxy:
                    #     proxy = _proxy()
                    #     print('正在使用代理{}，抓取页面 {}'.format(proxy, url))
                    #     try:
                    #         response1 = requests.get(url, headers=get_proxy_headers(proxy), proxies=proxy, timeout=spider_timeout)
                    #     except Exception as e:
                    #         response1 = retry_crawl(url, is_proxy)
                    # else:
                    #     try:
                    #         response1 = requests.get(url, headers=get_headers(), timeout=spider_timeout)
                    #     except Exception as e:
                    #         response1 = retry_crawl(url, is_proxy)
                    # _response1 = response1.text
                    # 此处使用selenium爬取页面，解决页面返回没有数据的问题
                    _response1 = selenium_crawl(url, is_proxy)
                    if _response1 is not None:
                        _soup = BeautifulSoup(_response1, 'lxml')
                    # print(_soup)
                    data_list.append(_soup)
                    print("{}=============抓取成功！".format(name))
                except Exception as e:
                    logging.error(name + '=========================抓取该公司的信息异常')
                    error_data_list.append(name)
                    logging.error(e)
                    # print(str(e))
                    # logging.exception(e)
                # 导出excel
                if len(data_list) > 0 or len(error_data_list) > 0:
                    print('==================正在写入excel文件，请勿关闭程序！==================')
                    export_excel(data_list, error_data_list)
                time.sleep(random.randint(crawl_interval_mintime, crawl_interval_maxtime))  # 每隔5到20秒
    else:
        print('====================本程序只能在外网环境下运行====================')
    input('按任意键回车退出：')
