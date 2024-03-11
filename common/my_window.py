import _thread
import logging
import sys
from time import sleep

from cv2 import imread, matchTemplate, TM_CCOEFF_NORMED
import win32api
import win32con
import win32gui
from numpy import where as np_where

from PIL import ImageGrab, Image
from PyQt6.QtWidgets import QApplication
from win10toast import ToastNotifier

import dirs
from common import my_util, my_mouse

MODE_FG = 'fg'
MODE_BG = 'bg'


# 获取指定标题窗口句柄
def find(title):
    return win32gui.FindWindow(None, title)


# 获取屏幕尺寸
def get_screen_size():
    screen_w = win32api.GetSystemMetrics(0)
    screen_h = win32api.GetSystemMetrics(1)
    return screen_w, screen_h


# 由最小化恢复正常
def restore(hwnd=0):
    # win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)


# 设置目标窗口为活动窗口
def show(hwnd=0):
    restore(hwnd)
    # 需要解决不能连续SetForegroundWindow问题
    # win32api.keybd_event(18, 0, 0, 0)
    # time.sleep(0.01)
    win32gui.SetForegroundWindow(hwnd)


# 显示但不激活，不抢占前台
def show_noactive(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)


# 隐藏目标窗口以及托盘图标
def hide(hwnd=0):
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


# 最小化窗口
def minimize(hwnd=0):
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)


# 获取目标窗口尺寸
def get_size(hwnd=0):
    rect = win32gui.GetWindowRect(hwnd)
    target_w = rect[2] - rect[0]
    target_h = rect[3] - rect[1]
    return target_w, target_h


# 移动窗口到指定坐标
def moveto(hwnd=0, x=0, y=0):
    target_w, target_h = get_size(hwnd)
    win32gui.MoveWindow(hwnd, x, y, target_w, target_h, 1)


# 移动窗口到右上角
def move_rt(hwnd=0):
    screen_w, screen_h = get_screen_size()
    target_w, target_h = get_size(hwnd)
    win32gui.MoveWindow(hwnd, screen_w - target_w, 0, target_w, target_h, 1)


# 移动窗口到左上角
def move_lt(hwnd=0):
    target_w, target_h = get_size(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, target_w, target_h, 1)


# 重置窗口大小
def resize(hwnd=0, w=0, h=0):
    if w == 0 or h == 0:
        w, h = get_size(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, w, h, 1)


def capture(hwnd=0, mode=MODE_BG, loc_range=None, cap_path=None):
    if cap_path is None:
        cap_path = my_util.capture_path()
    x = 0
    y = 0
    w = -1
    h = -1
    if loc_range is not None:
        x, y = loc_range[0]
        end_x, end_y = loc_range[1]
        w = end_x - x
        h = end_y - y
    if mode == MODE_FG:
        capture_fg(hwnd, x, y, w, h).save(cap_path)
    else:
        if win32gui.IsIconic(hwnd):
            show_noactive(hwnd)
            logging.info('检测到目标窗口为最小化，将自动恢复')
        capture_bg(hwnd, x, y, w, h).save(cap_path)
    return cap_path


# 前台窗口截图，用于不支持后台操作的窗口
def capture_fg(hwnd=0, x=0, y=0, width=-1, height=-1):
    start_x = x
    start_y = y
    target_w = width
    target_h = height
    if width == -1:
        target_w, target_h = get_size(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    capture_img = ImageGrab.grab(
        (rect[0] + start_x, rect[1] + start_y, rect[0] + start_x + target_w, rect[1] + start_y + target_h))
    return capture_img


# 后台窗口截图，默认截全屏
def capture_bg(hwnd=0, x=0, y=0, width=-1, height=-1):
    screen = QApplication.primaryScreen()
    if screen is None:
        # QT应用由于已存在QApplication对象不能再调用此方法
        app = QApplication(sys.argv)
        screen = QApplication.primaryScreen()
    capture_img = screen.grabWindow(hwnd, x, y, width, height).toImage()
    return capture_img


def enum_all(class_name=None, name=None):
    def _get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            # print(f'{hwnd}:{win32gui.GetWindowText(hwnd)}:{win32gui.GetClassName(hwnd)}:{win32gui.GetParent(hwnd)}')
            if class_name is None and name is None:
                temp.update({hwnd: win32gui.GetWindowText(hwnd)})
            elif class_name is not None:
                if class_name == win32gui.GetClassName(hwnd):
                    temp.update({hwnd: win32gui.GetWindowText(hwnd)})
            elif name is not None:
                if name == win32gui.GetWindowText(hwnd):
                    temp.update({hwnd: win32gui.GetWindowText(hwnd)})

    temp = dict()
    win32gui.EnumWindows(_get_all_hwnd, 0)
    return temp


# 枚举所有子窗口
def enum_child(parent_hwnd=0):
    def _get_children_hwnd(hwnd, param):
        temp.update({hwnd: win32gui.GetClassName(hwnd)})

    temp = dict()
    win32gui.EnumChildWindows(parent_hwnd, _get_children_hwnd, None)
    return temp


# 关闭窗口
def close(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


# 在窗口内查找图片，返回所有坐标
def find_pic_multi(hwnd=0, mode=MODE_BG, template_path=None, match_ratio=0.8, loc_range=None, do_capture=True):
    if do_capture:
        capture(hwnd, mode, loc_range)
    match_list = match(template_path, my_util.capture_path(), match_ratio)
    # 相邻位置仅保留1个，周围几个像素会被重复匹配
    filter_list = []
    for loc1 in match_list:
        exists = False
        for loc2 in filter_list:
            if abs(loc2[0] - loc1[0]) < 5 and abs(loc2[1] - loc1[1]) < 5:
                exists = True
                break
        if not exists:
            filter_list.append(loc1)
    base_x, base_y = (0, 0) if loc_range is None else (loc_range[0][0], loc_range[0][1])
    if do_capture:
        return [(base_x + loc[0], base_y + loc[1]) for loc in filter_list]
    return filter_list


# 匹配返回所有坐标
def match(tmp_path, cap_path, match_ratio):
    match_rgb = imread(cap_path)
    template_rgb = imread(tmp_path)
    res = matchTemplate(match_rgb, template_rgb, TM_CCOEFF_NORMED)
    loc = np_where(res > match_ratio)
    zipped = zip(*loc[::-1])
    listed = list(zipped)
    return listed


# 在窗口内查找图片，返回第一个匹配的坐标
def find_pic(hwnd=0, mode=MODE_BG, template_path=None, match_ratio=0.8, loc_range=None, do_capture=True):
    listed = find_pic_multi(hwnd, mode, template_path, match_ratio, loc_range, do_capture=do_capture)
    result = None
    if len(listed) > 0:
        result = listed[0]
    return result


# 查找并单击图标
def find_click(hwnd=0, mode=MODE_BG, template_path=None, match_ratio=0.8, loc_range=None, do_capture=True):
    loc = find_pic(hwnd, mode, template_path, match_ratio, loc_range, do_capture=do_capture)
    if loc is not None:
        my_mouse.left_click(hwnd, (loc[0] + 10, loc[1] + 10))
        sleep(1)
    return loc


# 在窗口内查找所给图片集合中的任一图片并返回第一个匹配的坐标
def find_any_pic(hwnd=0, mode=MODE_BG, template_paths=None, match_ratio=0.8, loc_range=None, do_capture=True):
    if template_paths is None:
        template_paths = []
    if do_capture:
        capture(hwnd, mode, loc_range)
    for template_path in template_paths:
        listed = match(template_path, my_util.capture_path(), match_ratio)
        if len(listed) > 0:
            result = listed[0]
            base_x, base_y = (0, 0) if loc_range is None else (loc_range[0][0], loc_range[0][1])
            if do_capture:
                return base_x + result[0], base_y + result[1]
            return result
    return None


# 指定窗口内等待图片出现
def wait_appear(hwnd=0, mode=MODE_BG, template_path=None, match_ratio=0.8, timeout=5, loc_range=None):
    for i in range(0, timeout * 2):
        loc = find_pic(hwnd, mode, template_path, match_ratio, loc_range=loc_range)
        if loc is not None:
            return loc
        sleep(0.5)
    return None


# 等待图片出现并单击
def wait_click(hwnd=0, mode=MODE_BG, template_path=None, match_ratio=0.8, timeout=5, loc_range=None):
    loc = wait_appear(hwnd, mode, template_path, match_ratio, timeout, loc_range=loc_range)
    if loc is not None:
        my_mouse.left_click(hwnd, (loc[0] + 10, loc[1] + 10))
        sleep(1)
    return loc


def wait_any_appear(hwnd=0, mode=MODE_BG, template_paths=None, match_ratio=0.8, timeout=5, loc_range=None):
    for i in range(0, timeout):
        loc = find_any_pic(hwnd, mode, template_paths, match_ratio, loc_range=loc_range)
        if loc is not None:
            return loc
        sleep(1)
    return None


# 截图
# def window_api_capture(file, hwnd=0):
#     if hwnd == 0:
#         monitor_dev = win32api.EnumDisplayMonitors(None, None)
#         width = monitor_dev[0][2][2]
#         height = monitor_dev[0][2][3]
#     else:
#         left, top, right, bot = win32gui.GetWindowRect(hwnd)
#         width = right - left
#         height = bot - top
#         # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
#     hwnd_dc = win32gui.GetWindowDC(hwnd)
#     # 创建设备描述表
#     mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
#     # 创建内存设备描述表
#     save_dc = mfc_dc.CreateCompatibleDC()
#     # 创建位图对象准备保存图片
#     save_bitmap = win32ui.CreateBitmap()
#     # 为bitmap开辟存储空间
#     save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
#     # 将截图保存到saveBitMap中
#     save_dc.SelectObject(save_bitmap)
#     # 保存bitmap到内存设备描述表
#     save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
#     try:
#         save_bitmap.SaveBitmapFile(save_dc, file)
#     except:
#         pass
#     win32gui.DeleteObject(save_bitmap.GetHandle())
#     save_dc.DeleteDC()
#     mfc_dc.DeleteDC()
#     win32gui.ReleaseDC(hwnd, hwnd_dc)


# 置顶
def force_focus(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOOWNERZORDER | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


# 取消置顶
def cancel_focus(hwnd):
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                          win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


# 展示图片
def show_img(img_path):
    img = Image.open(img_path)
    img.show()


# 输入文本
def send_msg(hwnd=0, words=None):
    for word in words:
        win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(word), 0)
        sleep(0.01)


# 发送系统通知，持续时间默认5秒设置无效
def notify(title, msg, icon_path=dirs.join_data('logo.ico')):
    toast = ToastNotifier()
    _thread.start_new_thread(toast.show_toast, (title, msg, icon_path))
    sleep(0.2)


# 获取窗口起始坐标
def get_wnd_loc(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect[0], rect[1]
