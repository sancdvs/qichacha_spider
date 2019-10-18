# 目标采集地址
base_url1 = 'http://m.qichacha.com'
base_url = 'http://m.qichacha.com/search?key='
# 爬取目标页面超时时间
spider_timeout = 30
# 爬取目标页面重试次数
spider_retry_num = 3
# 生成cookie网址
generate_cookie_url = 'https://www.qichacha.com/user_login'
# generate_cookie_url = 'https://m.qichacha.com/user_login'
# 设置获取最大cookie数量
cookie_max_num = 5
# 获取cookie超时时间
cookie_timeout = 10
# 获取cookie重试次数
cookie_retry_num = 5
# 获取cookie批次的间隔时间(秒)
cookie_interval_time = 60*30
# 获取代理ip地址，这边需要本地部署一个提供代理IP的应用，这里使用的是proxy_list-master
proxy_ip_url = 'http://127.0.0.1:8111/proxy?count=10'
# proxy_ip_url = 'http://127.0.0.1:8111/proxy'
# 搜索企业文件名称
enterprise_search_file = r'./enterprise_search.txt'
# phantomjs驱动
phantomjs_driver = r'\phantomjs-2.1.1-windows\bin\phantomjs.exe'
# chrome驱动
chrome_driver = r'.\chromedriver_win32\chromedriver.exe'
# 日志目录
log_dir = r'\logs'
