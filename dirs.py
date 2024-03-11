import os
import sys

'''
冻结路径
'''


def app_path():
    if getattr(sys, 'frozen', False):
        target_dir = sys._MEIPASS
    else:
        target_dir = os.path.dirname(os.path.abspath(__file__))
    return target_dir


def assets_path():
    return os.path.join(app_path(), 'assets')


def data_path():
    return os.path.join(assets_path(), 'data')


def join_data(name):
    return os.path.join(data_path(), name)


def templates_path():
    return os.path.join(assets_path(), 'templates')


def join_template(name):
    return os.path.join(templates_path(), name)
