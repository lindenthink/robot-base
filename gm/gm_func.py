# 获取窗口
import logging
import time
import gm.gm_con as con

from common import my_window, my_mouse, my_util, my_cfg


def get_hwnd():
    meta = my_cfg.loadMeta()
    return my_window.find(meta['name'])


# 检测窗口是否存在注解
def check_wnd(func):
    def fun(*args, **kwargs):
        while True:
            hwnd = get_hwnd()
            if hwnd < 1:
                logging.info('检测到目标窗口不存在，将尝试重新打开...')
                # todo 重新打开
            result = func(*args, **kwargs)
        return result

    return fun


# 刷新登陆
def refresh(hwnd=0, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, (350, 25))
    time.sleep(1)
    my_mouse.left_click(hwnd, (215, 270))
    time.sleep(2)
    my_util.retry(get_hwnd, 10)
    hwnd = get_hwnd()
    if not hwnd:
        logging.info('超时未获取到目标窗口，将尝试重新打开...')
        return False
    my_window.move_lt(hwnd)
    time.sleep(0.5)
    my_window.show(hwnd)
    time.sleep(0.5)
    # 等待加载资源
    time.sleep(3)
    return True
