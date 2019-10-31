import inspect
import logging
import os
from config import log_dir

'''日志配置'''
# 获取当前文件路径
current_path = inspect.getfile(inspect.currentframe())
# 获取当前文件所在目录，相当于当前文件的父目录
dir_name = os.path.dirname(current_path)
# 转换为绝对路径
file_abs_path = os.path.abspath(dir_name)
log_file_path = file_abs_path+log_dir+r'\app.log'
# print(log_file_path)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"    # 日志格式化输出
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"                        # 日期格式
# fp = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')   # 覆盖
fp = logging.FileHandler(log_file_path, encoding='utf-8')               # 追加
fs = logging.StreamHandler()
logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])    # 调用