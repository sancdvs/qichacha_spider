# -*- coding: UTF-8 -*-
import json
import random
import time
import csv
import urllib
from importlib import reload

from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from openpyxl import load_workbook
import sys

# reload(sys)
# exec("sys.setdefaultencoding('utf-8')")

from config import chrome_driver
from headers import user_agent
from tools.chaojiying import Chaojiying_Client

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-agent='+random.choice(user_agent))
# chrome_options.add_argument('--headless')  # 开启无界面模式
# chrome_options.add_argument('--disable-gpu')  # 禁用gpu，解决一些莫名的问题
# chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)
# driver = webdriver.Chrome(executable_path=chrome_driver)
driver.maximize_window()


def save():
    img = driver.find_element_by_xpath('//div[@class="imgCaptcha_img"]/img')
    img_url = img.get_attribute("src")
    data = urllib.urlopen(img_url).read()
    f = open('a.jpg', 'wb')
    f.write(data)


def chaoji():
    chaojiying = Chaojiying_Client('sunlu123', 'sl123456', '901903')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    datas = chaojiying.PostPic(im, 1902)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    ocr = datas['pic_str']
    # print datas
    print(ocr)
    return ocr


# 用于提供模拟匀加速运动的轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 5
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 3
        else:
            a = 6
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    print(track)
    return track


# 滑动验证码识别
def slide_discern():
    print("滑块验证码验证中。。。")
    # try:
    # 获取到需滑动的按钮
    source = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')
    action = ActionChains(driver)
    # 按住左键不放
    action.click_and_hold(source).perform()
    # 开始滑动
    distance = 348  # 模拟以人为速度拖动
    track = get_track(distance)
    # ttt = [23, 81, 224]
    for i in track:
        try:
            action.move_by_offset(xoffset=i, yoffset=0).perform()   # perform --- 执行所有准备好的Action
            # action.reset_actions()  # reset_actions --- 清空所有准备好的Action,这个需要selenium版本3.0以上
            # time.sleep(0.4)
        except StaleElementReferenceException as e:
            action.release().perform()  # 释放鼠标
            driver.find_element_by_xpath('//div[@class="errloading"]/span/a').click()
            source = driver.find_element_by_xpath('//*[@id="nc_1_n1z"]')    # 获取到需滑动的按钮
            action = ActionChains(driver)
            action.click_and_hold(source).perform() # 按住左键不放
            # action.reset_actions()  # 清除之前的action
            action.move_by_offset(xoffset=i, yoffset=0).perform()  # perform --- 执行所有准备好的Action
    # 释放鼠标
    action.release().perform()


def login_web():
    # 打开企查查登录网页
    driver.get("https://www.qichacha.com/user_login")
    # 加载时间
    # time.sleep(3)
    # 点击密码登录
    driver.find_element_by_xpath('//div[@class="login-panel-head clearfix"]/div[2]').click()
    time.sleep(1)
    # 找到账号输入框
    driver.find_element_by_xpath('//div[@class="form-group"]/input[@id="nameNormal"]').send_keys('15256017820')
    time.sleep(1)
    # 找到密码输入框
    driver.find_element_by_xpath('//div[@class="form-group m-t-md"]/input[@id="pwdNormal"]').send_keys('sl123456')
    time.sleep(1)
    slide_discern()
    # 滑动条定位
    # start = driver.find_element_by_xpath('//div[@id="nc_1_n1t"]/span')
    # 长按拖拽
    # action = ActionChains(driver)
    # 长按
    # action.click_and_hold(start)
    # 拉动
    # action.drag_and_drop_by_offset(start, 320, 0).perform()
    time.sleep(5)
    # 保存图片
    # save()
    # 此处延时为了手动输入验证码（省钱。）
    # time.sleep(10)
    # 超级鹰识别验证码
    # ocr = chaoji()
    # # 输入验证码
    # driver.find_element_by_xpath('//div[@class="imgCaptcha_text"]/input').send_keys(ocr)
    # # 点击提交
    # driver.find_element_by_xpath('//div[@id="nc_1_scale_submit"]/span').click()
    # 截图
    driver.save_screenshot('web.png')
    # 点击登录
    driver.find_element_by_xpath('//form[@id="user_login_normal"]/button').click()
    # time.sleep(3)
    # 关闭弹窗
    # driver.find_element_by_xpath('//div[@class="bindwx"]/button/span[1]').click()
    cookie_list = driver.get_cookies()
    print(cookie_list)

def run():
    # 读取本地文件
    with open('data.json', encoding='utf-8') as f:
        datas = json.load(f)
        data_list = []
        for i in datas:
            data = i[u"企业名称"].encode('utf-8').decode('utf-8')
            number = i[u"统一社会信用代码"].encode('utf-8')
            # print data
            # print type(data)
            try:
                # 输入公司名
                driver.find_element_by_xpath('//div[@class="input-group"]/input[@name="key"]').send_keys(data)
                time.sleep(1)
                # 点击搜索
                driver.find_element_by_xpath('//div[@class="input-group"]/span/input').click()
                # time.sleep(random.randint(1, 5))
            except Exception as e:
                # 切换回原窗口
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                # 删除原公司名
                driver.find_element_by_xpath('//div[@class="input-group"]/a').click()
                # time.sleep(random.randint(1, 3))
                # 输入下一个公司
                driver.find_element_by_xpath('//div[@class="input-group"]/input[@name="key"]').send_keys(data)
                time.sleep(1)
                # 点击搜索
                driver.find_element_by_xpath('//div[@class="input-group"]/span/button').click()
                # print driver.title
            # 点击第一条
            driver.find_element_by_xpath('//table[@class="m_srchList"]/tbody[@id="search-result"]/tr[1]/td[3]/a').click()
            # 获取当前窗体的列表
            # print(driver.window_handles)
            # 切换至第二个窗口
            driver.switch_to.window(driver.window_handles[1])
            # 此处做判断，输入公司是否包含法律风险
            aaa = driver.find_element_by_xpath('//div[@class="risk-panel b-a"]/a[2]').click()
            if aaa:
                # 点击查看风险
                driver.find_element_by_xpath('//div[@class="risk-panel b-a"]/a[2]').click()
                time.sleep(1)
                # 分析数据源
                # 自身风险
                url1 = driver.find_element_by_xpath('//div[@class="tab pull-left"]/a[1]').get_attribute('href')
                # 关联风险
                url2 = driver.find_element_by_xpath('//div[@class="tab pull-left"]/a[2]').get_attribute('href')
                # 提示信息
                url3 = driver.find_element_by_xpath('//div[@class="tab pull-left"]/a[3]').get_attribute('href')
                if url1:
                    # ----------------------------------------------    自身风险  ----------------------------------------------
                    # 点击界面
                    driver.find_element_by_xpath('//div[@class="tab pull-left"]/a[1]').click()
                    time.sleep(1)
                    print('{} 包含 自身风险 数据'.format(i[u"企业名称"].encode('utf-8')))
                    # 点击 裁判文书  id= judgementLis
                    judgementList = driver.find_elements_by_xpath('//div[@class="container"]/div[@id="judgementList"]/section/div')
                    ju = 0
                    # print type(books)
                    caipan_list = {}
                    if judgementList:
                        print('----------------------命中裁判文书----------------------')
                        for book in judgementList:
                            print(ju + 1)
                            time.sleep(1)
                            judgementList[ju].click()
                            # 此处必须加延时，等待网页JS渲染
                            time.sleep(1)
                            html_cai = etree.HTML(driver.page_source)
                            # print driver.page_source
                            # 弹窗内数据条数
                            caipan_len = driver.find_elements_by_xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr')
                            bananas = len(caipan_len)
                            print('裁判文书含有 {}条数据'.format(bananas - 1))
                            ban = 2
                            for banana in range(1, bananas):
                                try:
                                    # 案件名称
                                    titles_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[2]/a/text()'.format(ban))
                                    titles_caipan = titles_caipan[0].strip()
                                    print('案件名称：', titles_caipan)
                                    # 发布时间
                                    time_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[3]/text()'.format(ban))
                                    time_caipan = time_caipan[0].strip()
                                    print('发布时间：', time_caipan)
                                    # 案件编号
                                    num_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[4]/text()'.format(ban))
                                    num_caipan = num_caipan[0].strip()
                                    print('案件编号：', num_caipan)
                                    # 案件身份
                                    id_caipan = html_cai.xpath('string(//table[@class="ntable ntable-odd"]/tbody/tr[{}]/td[5])'.format(ban))
                                    # id_caipan = id_caipan[0].stirp()
                                    print('案件身份：', id_caipan)
                                    # 执行法院
                                    court_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[6]/text()'.format(ban))
                                    court_caipan = court_caipan[0].strip()
                                    print('执行法院：', court_caipan)
                                    ban += 1
                                except Exception as e:
                                    # 案件名称
                                    titles_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[2]/a/text()')
                                    titles_caipan = titles_caipan[0].strip()
                                    print('案件名称：', titles_caipan)
                                    # 发布时间
                                    time_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[3]/text()')
                                    time_caipan = time_caipan[0].strip()
                                    print('发布时间：', time_caipan)
                                    # 案件编号
                                    num_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[4]/text()')
                                    num_caipan = num_caipan[0].strip()
                                    print('案件编号：', num_caipan)
                                    # 案件身份
                                    id_caipan = html_cai.xpath('string(//table[@class="ntable ntable-odd"]/tbody/tr[2]/td[5])')
                                    id_caipan = id_caipan
                                    print('案件身份：', id_caipan[0].strip())
                                    # 执行法院
                                    court_caipan = html_cai.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[6]/text()')
                                    court_caipan = court_caipan[0].strip()
                                    print('执行法院：', court_caipan)
                                caipan_list['企业名称：'] = data
                                caipan_list['统一社会信用代码：'] = number
                                caipan_list['类型：'] = '法律风险'
                                caipan_list['标题：'] = titles_caipan
                                caipan_list['时间：'] = time_caipan
                                caipan_list[
                                    '内容：'] = '案件名称:' + titles_caipan + '\n' + '发布时间:' + time_caipan + '\n' + '案件编号:' + num_caipan + '\n' + '案件身份:' + id_caipan + '\n' + '执行法院:' + court_caipan
                                data_list.append(caipan_list)
                            # print '\n'
                            # 关闭弹窗
                            driver.find_element_by_xpath('//div[@class="modal fade in"]/div/div[@class="modal-content risk-modal-list"]/div/button').click()
                            ju += 1
                    # 点击 开庭公告  class= panel m-b-xs
                    notices = driver.find_elements_by_xpath('//div[@class="container"]/section[@class="panel m-b-xs"]/div')
                    no = 0
                    kaiting_list = {}
                    if notices:
                        print('----------------------命中开庭公告----------------------')
                        for notice in notices:
                            print(no + 1)
                            time.sleep(1)
                            notices[no].click()
                            # 此处必须加延时，等待网页JS渲染
                            time.sleep(1)
                            html_gonggao = etree.HTML(driver.page_source)
                            # print driver.page_source
                            # 弹窗内数据条数
                            notice_len = driver.find_elements_by_xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr')
                            apples = len(notice_len)
                            print('开庭公告含有 {}条数据'.format(apples - 1))
                            app = 2
                            for apple in range(1, apples):
                                try:
                                    # 案号
                                    id_gongao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[2]/a/text()'.format(app))
                                    id_gongao = id_gongao[0].strip()
                                    print('案号：', id_gongao)
                                    # 开庭日期
                                    time_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[3]/text()'.format(app))
                                    time_gonggao = time_gonggao[0].strip()
                                    print('开庭日期：', time_gonggao)
                                    # 案由
                                    reason_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[4]/text()'.format(app))
                                    reason_gonggao = reason_gonggao[0].strip()
                                    print('案由：', reason_gonggao)
                                    # 公诉人/原告/上诉人/申请人
                                    plaintiff_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[5]/text()'.format(app))
                                    plaintiff_gonggao = plaintiff_gonggao[0].strip()
                                    print('公诉人/原告/上诉人/申请人：', plaintiff_gonggao)
                                    # 被告人/被告/被上诉人/被申请人
                                    accused_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[{}]/td[6]/text()'.format(app))
                                    accused_gonggao = accused_gonggao[0].strip()
                                    print('被告人/被告/被上诉人/被申请人：', accused_gonggao)
                                    app += 1
                                except Exception as e:
                                    # 案号
                                    id_gongao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[2]/a/text()')
                                    id_gongao = id_gongao[0].strip()
                                    print('案号：', id_gongao)
                                    # 开庭日期
                                    time_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[3]/text()')
                                    time_gonggao = time_gonggao[0].strip()
                                    print('开庭日期：', time_gonggao)
                                    # 案由
                                    reason_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[4]/text()')
                                    reason_gonggao = reason_gonggao[0].strip()
                                    print('案由：', reason_gonggao)
                                    # 公诉人/原告/上诉人/申请人
                                    plaintiff_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[5]/text()')
                                    plaintiff_gonggao = plaintiff_gonggao[0].strip()
                                    print('公诉人/原告/上诉人/申请人：', plaintiff_gonggao)
                                    # 被告人/被告/被上诉人/被申请人
                                    accused_gonggao = html_gonggao.xpath('//div[@class="modal-body"]/section/div[2]/table/tbody/tr[2]/td[6]/text()')
                                    accused_gonggao = accused_gonggao[0].strip()
                                    print('被告人/被告/被上诉人/被申请人：{}'.format(accused_gonggao))
                                kaiting_list['企业名称：'] = data
                                kaiting_list['统一社会信用代码：'] = number
                                kaiting_list['类型：'] = '法律风险'
                                kaiting_list['标题：'] = reason_gonggao
                                kaiting_list['时间：'] = time_gonggao
                                kaiting_list[
                                    '内容：'] = '案号:' + id_gongao + '\n' + '开庭日期:' + time_gonggao + '\n' + '案由:' + reason_gonggao + '\n' + '公诉人/原告/上诉人/申请人:' + plaintiff_gonggao + '\n' + '被告人/被告/被上诉人/被申请人:' + accused_gonggao
                                data_list.append(kaiting_list)
                            # print '\n'
                            # 关闭弹窗
                            driver.find_element_by_xpath('//div[@class="modal fade in"]/div/div[@class="modal-content risk-modal-list"]/div/button').click()
                            no += 1
                    # 点击 行政处罚  id= apList
                    # 点击 税务行政处罚  id= tpList

                    time.sleep(random.randint(1, 3))
                if url2:
                    print('{} 包含 关联风险 数据'.format(i[u"企业名称"].encode('utf-8')))
                    # 点击 股权出质  id= PledgeList
                    # 点击 法定代表人变更 id= OperList
                    # 点击 大股东变更 id= PartnerList
                    # 点击 严重违法 id= SeriousViolation
                    # 点击 经营异常 id= ExceptionList
                    # 点击 失信被执行人 id= shixinList
                    # 点击 被执行人 id= zhixingList
                    # 点击 限制消费 id= stList
                    time.sleep(random.randint(1, 3))
                if url3:
                    print('{} 包含 提示信息 数据'.format(i[u"企业名称"].encode('utf-8')))
                    # 点击 法定代表人变更  section> class= panel m-b-xs
                    # 点击 大股东变更  section> class= panel m-b-xs
            else:
                print('{} 该公司没有风险提示'.format(i[u"企业名称"].encode('utf-8')))
            # 关闭页面换家公司
            driver.close()
            # 切换回原窗口
            driver.switch_to.window(driver.window_handles[0])
            # time.sleep(random.randint(1, 5))

            # 写入本地文件
            with open('111.json', 'w') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)
            # wb可以解决python2 没有newline='',否则数据出现每行空一行
            with open('111.csv', 'wb') as f:
            # 通过文件对象创建 csv 写入对象
                csv_writer = csv.writer(f)
                # 写入标题
                csv_writer.writerow(data_list[0].keys())
                # # 写入内容
                for row in data_list:
                    csv_writer.writerow(row.values())
                    # l = [i.decode('utf8').encode('gbk') for i in row.values()]
                    # csv_writer.writerow(l)
                f.close()


if __name__ == '__main__':
    login_web()
    # run()