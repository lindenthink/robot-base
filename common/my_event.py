# coding=utf-8
from ctypes import *
from ctypes import wintypes

import win32con
from PyQt6.QtCore import QThread

SetWindowsHookEx = windll.user32.SetWindowsHookExA
UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx
CallNextHookEx = windll.user32.CallNextHookEx
GetMessage = windll.user32.GetMessageA
GetModuleHandle = windll.kernel32.GetModuleHandleW


class KbdHookStruct(Structure):
    _fields_ = [
        ('vkCode', c_int),
        ('scanCode', c_int),
        ('flags', c_int),
        ('time', c_int),
        ('dwExtraInfo', c_uint),
        ('', c_void_p)
    ]


class Point(Structure):
    _fields_ = [
        ('x', c_long),
        ('y', c_long)
    ]


class MouseHookStruct(Structure):
    _fields_ = [
        ('pt', Point),
        ('hwnd', c_int),
        ('wHitTestCode', c_uint),
        ('dwExtraInfo', c_uint),
    ]


class MyEvent:
    # 保存键盘钩子函数句柄
    kbd_hd = None
    # 保存鼠标钩子函数句柄
    mouse_hd = None
    # 触发函数
    on_trigger = None

    def __init__(self, on_trigger):
        self.on_trigger = on_trigger

    @staticmethod
    def wait_for_msg():
        msg = wintypes.MSG()
        GetMessage(msg, 0, 0, 0)

    def keyboard_pro(self, nCode, wParam, lParam):
        """
        函数功能：键盘钩子函数，当有按键按下时此函数被回调
        """
        if nCode == win32con.HC_ACTION:
            kbd_p = POINTER(KbdHookStruct)
            param = cast(lParam, kbd_p)
            self.on_trigger(vk_code=param.contents.vkCode)
            # print(param.contents.vkCode)
        return CallNextHookEx(self.kbd_hd, nCode, wParam, lParam)

    def start_keyboard_hook(self):
        """
        函数功能：启动键盘监听
        """
        func_type = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        p = func_type(self.keyboard_pro)
        self.kbd_hd = SetWindowsHookEx(
            win32con.WH_KEYBOARD_LL,
            p,
            GetModuleHandle(None),
            0)
        MyEvent.wait_for_msg()

    def stop_keyboard_hook(self):
        """
        函数功能：停止键盘监听
        """
        UnhookWindowsHookEx(self.kbd_hd)

    def mouse_pro(self, nCode, wParam, lParam):
        """
        函数功能：鼠标钩子函数，当有鼠标事件，此函数被回调
        """
        if nCode == win32con.HC_ACTION:
            mouse_p = POINTER(MouseHookStruct)
            param = cast(lParam, mouse_p)
            self.on_trigger(vk_code=wParam, x=param.contents.pt.x, y=param.contents.pt.y)
            # 鼠标左键点击
            if wParam == win32con.WM_LBUTTONDOWN:
                print("左键点击，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_LBUTTONUP:
                print("左键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
                self.stop_mouse_hook()
            elif wParam == win32con.WM_MOUSEMOVE:
                print("鼠标移动，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_RBUTTONDOWN:
                print("右键点击，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
            elif wParam == win32con.WM_RBUTTONUP:
                print("右键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
        return CallNextHookEx(self.mouse_hd, nCode, wParam, lParam)

    def start_mouse_hook(self):
        """
        函数功能：启动鼠标监听
        """
        func_type = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        p = func_type(self.mouse_pro)
        self.mouse_hd = SetWindowsHookEx(
            win32con.WH_MOUSE_LL,
            p,
            GetModuleHandle(None),
            0)
        MyEvent.wait_for_msg()

    def stop_mouse_hook(self):
        """
        函数功能：停止鼠标监听
        """
        UnhookWindowsHookEx(self.mouse_hd)


class MouseListener(QThread):
    e = None
    onTrigger = None

    def __init__(self, onTrigger):
        super().__init__()
        self.onTrigger = onTrigger

    def run(self):
        self.e = MyEvent(self.onTrigger)
        self.e.start_mouse_hook()

    def stop(self):
        self.e.stop_mouse_hook()
