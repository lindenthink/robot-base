from time import sleep

import win32api
import win32con
import win32gui
from numpy import linspace


# 左键在指定位置单击
def left_click(hwnd=0, loc=(0, 0)):
    x, y = loc
    target_pos = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, target_pos)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, target_pos)


# 前台单击鼠标-相对坐标
def left_click_fg(hwnd=0, loc=(0, 0)):
    rect = win32gui.GetWindowRect(hwnd)
    relative_loc = (rect[0] + loc[0], rect[1] + loc[1])
    left_click_fg_ab(relative_loc[0], relative_loc[1])


# 前台点击鼠标-绝对坐标
def left_click_fg_ab(x, y):
    win32api.SetCursorPos([x, y])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 左键拖拽
def left_drag(hwnd=0, pos1=(), pos2=(), num=20):
    move_x = linspace(pos1[0], pos2[0], num)[0:]
    move_y = linspace(pos1[1], pos2[1], num)[0:]
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         0, win32api.MAKELONG(pos1[0], pos1[1]))
    for i in range(num):
        x = int(round(move_x[i]))
        y = int(round(move_y[i]))
        move_to(hwnd, (x, y))
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP,
                         0, win32api.MAKELONG(pos2[0], pos2[1]))


# 左键按下并在指定时间后弹起
def left_down_up(hwnd=0, x=0, y=0, delay=1):
    target_pos = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, target_pos)
    sleep(delay)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, target_pos)
    sleep(0.1)


def move_to(hwnd=0, loc=(0, 0)):
    win32gui.SendMessage(
        hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(loc[0], loc[1]))
    sleep(0.05)


# 右键在指定位置单击
def right_click(hwnd, loc=None):
    x, y = loc
    target_pos = win32api.MAKELONG(x, y)
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, target_pos)
    win32gui.SendMessage(hwnd, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, target_pos)


# 单击向下箭头
def down_click(hwnd):
    key_click(hwnd, win32con.VK_DOWN)


# 单击向上箭头
def up_click(hwnd):
    key_click(hwnd, win32con.VK_UP)


# 单击Enter
def enter_click(hwnd):
    key_click(hwnd, win32con.VK_RETURN)


# 键盘按键
def key_click(hwnd, vk=None):
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, vk)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, vk)
