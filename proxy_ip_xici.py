import requests
from lxml import etree
from urllib.parse import urljoin
import xlwt
import time
from excel_util import style_title, style
from headers import random_user_agent

# 导出代理ip到excel
workbook = xlwt.Workbook(encoding="utf-8")
worksheet = workbook.add_sheet("代理IP信息", cell_overwrite_ok=True)
worksheet.write(0, 0, "IP地址", style_title)
worksheet.write(0, 1, "端口", style_title)
worksheet.write(0, 2, "类型", style_title)
worksheet.write(0, 3, "速度", style_title)
worksheet.write(0, 4, "存活时间", style_title)
worksheet.col(0).width = 256 * 20


class MyException(Exception):

    def __init__(self, status, msg):
        self.status = status
        self.msg = msg
        super().__init__()


class XiCi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": random_user_agent(),
            "Host": "www.xicidaili.com"
        }
        self.row_num = 0

    def get_page_html(self, api):
        '''通过get方法请求网页'''
        response = self.session.get(url=api, headers=self.session.headers)
        # print(response.text)
        if response.status_code == 200:
            return response

    def __html_to_etree(self, html):
        '''将html源码转为xml'''
        return etree.HTML(html)

    def get_next_page_url(self, response):
        '''拿到下一页的url'''
        selector = self.__html_to_etree(response.text)
        try:
            next_page_url = selector.xpath("//a[@class='next_page']/@href")[0]
            next_page_url = urljoin(response.url, next_page_url)
            return next_page_url
        except IndexError:
            raise MyException(1000, "爬取完毕")

    def __get_proxies_info(self, response):
        '''获取到爬取的代理信息'''
        selector = self.__html_to_etree(response.text)
        tr_ele_list = selector.xpath("//*[@id='ip_list']//tr")
        for tr in tr_ele_list:
            ip = tr.xpath("td[2]/text()")
            if not ip:
                continue
            ip = ip[0]
            port = tr.xpath("td[3]/text()")[0]
            type = tr.xpath("td[6]/text()")[0]
            fast = tr.xpath("td[7]/div/@title")[0]
            life = tr.xpath("td[9]/text()")[0]
            if '天' in life or '小时' in life or ('分钟' in life and int(life[:-2]) > 30):
                yield [ip, port, type, fast, life]

    def __detect_availability(self, data):
        '''拿到爬取的数据，检测代理是否可以使用'''
        https_api = "https://icanhazip.com/"
        http_api = "http://icanhazip.com/"
        ip = data[0]
        port = data[1]
        type = data[2]
        proxies = {type.lower(): "{}://{}:{}".format(type.lower(), ip, port)}
        try:
            if type.upper() == "HTTPS":
                requests.get(https_api, headers={"User-Agent": random_user_agent()}, proxies=proxies, timeout=3)
            else:
                requests.get(http_api, headers={"User-Agent": random_user_agent()}, proxies=proxies, timeout=3)
            return True
        except Exception:
            return False

    def get_usable_proxies_ip(self, response):
        '''获取到可用的代理ip'''
        res = self.__get_proxies_info(response)
        # print(res)
        for data in res:
            if self.__detect_availability(data):
                self.save_proxy_to_excel(data)
                print("可用代理ip======================="+str(data))

    def save_proxy_to_excel(self, data):
        '''保存代理ip'''
        self.row_num += 1
        ip = data[0]
        port = data[1]
        type = data[2]
        fast = data[3]
        life = data[4]
        worksheet.write(self.row_num, 0, ip, style)
        worksheet.write(self.row_num, 1, port, style)
        worksheet.write(self.row_num, 2, type, style)
        worksheet.write(self.row_num, 3, fast, style)
        worksheet.write(self.row_num, 4, life, style)
        export_excel_name = 'proxy_ip_info.xls'
        workbook.save(export_excel_name)

    def run(self, api):
        '''启动入口'''
        page = 1
        i = 0
        while i < 10:
            print("爬取第{}页数据...".format(page))
            response = self.get_page_html(api)
            self.get_usable_proxies_ip(response)
            try:
                api = self.get_next_page_url(response)
            except MyException as e:
                if e.status == 1000:
                    print(e.msg)
                    break
            page += 1
            time.sleep(3)
            i += 1



if __name__ == '__main__':
    api = "https://www.xicidaili.com/nn"
    xici = XiCi()
    xici.run(api)