import logging
import time
from os import path, mkdir
from shutil import rmtree
from datetime import datetime, timedelta

FMT_DATETIME = '%Y-%m-%d %H:%M:%S'
FMT_DATE = '%Y-%m-%d'
FMT_TIME_HMS = '%H:%M:%S'
FMT_TIME_HM = '%H:%M'


def fmtDateTime(date=None):
    if date is None:
        date = datetime.now()
    return fmt(date, FMT_DATETIME)


def fmtDate(date=None):
    if date is None:
        date = datetime.now()
    return fmt(date, FMT_DATE)


def fmtTime(date=None):
    if date is None:
        date = datetime.now()
    return fmt(date, FMT_TIME_HM)


def fmt(date, fmt):
    return date.strftime(fmt)


def parseDateTime(dateTimeStr):
    return parse(dateTimeStr, FMT_DATETIME)


def parseDate(dateStr):
    return parse(dateStr, FMT_DATE)


def parseTime(timeStr):
    return parse(timeStr, FMT_TIME_HM)


def parse(dateStr, fmt):
    return datetime.strptime(dateStr, fmt)


def addDays(date, days=1):
    return date + timedelta(days=days)


def addHours(date, hours=1):
    return date + timedelta(hours=hours)


def addMinutes(date, minutes=1):
    return date + timedelta(minutes=minutes)


def baseDir():
    user_home = path.expanduser('~')
    base_path = path.join(user_home, '.linden')
    if not path.exists(base_path):
        mkdir(base_path)
    return base_path


# 截屏图片路径
def capture_path():
    match_path = path.join(baseDir(), 'capture.jpg')
    return match_path


def workDir():
    target = path.join(baseDir(), 'temp')
    if not path.exists(target):
        mkdir(target)
    return target


# 临时截屏片路路径
def temp_capture_path():
    match_path = path.join(baseDir(), 'temp_capture.jpg')
    return match_path


def joinWorkDir(name):
    return path.join(workDir(), name)


def clearWorkDir():
    base_path = path.join(baseDir(), '.linden')
    target = path.join(base_path, 'temp')
    if path.exists(target):
        # 删除非空目录
        rmtree(target)


def retry(func, count=5, **kwargs):
    num = 0
    result = False
    while not result and num < count:
        result = func(**kwargs)
        num += 1
        time.sleep(1)
    return result


def sleep(seconds=1, delay_factor=1):
    time.sleep(seconds * delay_factor)


# 耗时统计注解: @time_cost
def time_cost(func):
    def fun(*args, **kwargs):
        t = time.perf_counter()
        result = func(*args, **kwargs)
        logging.info(f'函数:{func.__name__}，耗时:{time.perf_counter() - t:.8f} s')
        return result

    return fun


# 当前是周几
def weekday():
    return datetime.now().weekday() + 1


# 判断当前时间是否在给定时间范围内
def in_progress(begin, end):
    now = fmtTime()
    return begin <= now <= end
