# -*- coding: utf-8 -*-
# ==================================================
# 对 Timer 做以下再封装的目的是：当某个功能需要每隔一段时间被
# 执行一次的时候，不需要在回调函数里对 Timer 做重新安装启动
# ==================================================
import inspect

from headers import generateCookie

__author__ = 'sunlu'

from threading import Timer, Thread
from datetime import datetime
import time,os
import multiprocessing
# 开启子进程是不支持打包exe文件的，所以会不停向操作系统申请创建子进程，导致内存炸了，multiprocessing.freeze_support()就是解决这个问题的
multiprocessing.freeze_support()


class MyTimer(Thread):
    def __init__(self, desc, interval_seconds, callback, args=None, kwargs=None):
        super().__init__()
        self._desc = desc
        self.__interval_seconds = interval_seconds
        self.__callback = callback
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}
        self._stop = False

    def run(self):
        while True:
            if not self._stop:
                # print('{}定时任务开始执行========================{}'.format(self._desc, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.__callback(*self.__args)
                time.sleep(self.__interval_seconds)
            else:
                break

    def cancel(self):
        self._stop = True

# class MyTimer(object):
#     def __init__( self, start_time, interval, callback_proc, args=None, kwargs=None ):
#
#         self.__timer = None
#         self.__start_time = start_time
#         self.__interval = interval
#         self.__callback_pro = callback_proc
#         self.__args = args if args is not None else []
#         self.__kwargs = kwargs if kwargs is not None else {}
#
#     def exec_callback( self, args=None, kwargs=None ):
#         self.__callback_pro( *self.__args, **self.__kwargs )
#         self.__timer = Timer( self.__interval, self.exec_callback )
#         self.__timer.start()
#
#     def start( self ):
#         interval = self.__interval - ( datetime.now().timestamp() - self.__start_time.timestamp() )
#         print(interval)
#         self.__timer = Timer(interval, self.exec_callback)
#         self.__timer.start()
#
#     def cancel( self ):
#         self.__timer.cancel()
#         self.__timer = None
    
# class AA:
#     def hello( self, name, age ):
#         print( "[%s]\thello %s: %d\n" % ( datetime.now().strftime("%Y%m%d %H:%M:%S"), name, age ) )


# def re_exe(callback,args=None, inc = 60):
#   while True:
#     callback(*args)
#     time.sleep(inc)

if __name__ == "__main__":
    timer = MyTimer('获取cookie', 5, generateCookie)
    timer.start()
    # re_exe("echo %time%", 5)
    # aa = AA()
    # re_exe(aa.hello, ["owenliu", 18], 5)
    # start = datetime.now().replace(minute=3, second=0, microsecond=0)
    # start = datetime.now()
    # print(start)
    # tmr = MyTimer(start, 5, aa.hello, ["owenliu", 18])
    # tmr.start()
    # tmr.cancel()