import win32api
import win32con
import win32gui


# 字符按键
def key_click(hwnd=0, key=''):
    key = key.upper()
    key_num = ord(key)
    num = win32api.MapVirtualKey(key_num, 0)
    down_param = 1 | (num << 16)
    up_param = 1 | (num << 16) | (1 << 30) | (1 << 31)
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, None, down_param)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, None, up_param)


# 字符键按下
def key_down(hwnd=0, key=''):
    key = key.upper()
    key_num = ord(key)
    num = win32api.MapVirtualKey(key_num, 0)
    down_param = 1 | (num << 16)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, None, down_param)


# 字符键弹起
def key_up(hwnd=0, key=''):
    key = key.upper()
    key_num = ord(key)
    num = win32api.MapVirtualKey(key_num, 0)
    up_param = 1 | (num << 16) | (1 << 30) | (1 << 31)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, None, up_param)


# 组合按键
def click_keys(hwnd, *args):
    for arg in args:
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, arg, 0)
    for arg in args:
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, arg, 0)


if __name__ == '__main__':
    target_hwnd = win32gui.FindWindow('WeChatMainWndForPC', '微信')
    print(target_hwnd)
    # key_num = ord('Q')
    # num = win32api.MapVirtualKey(key_num, 0)
    key_click(target_hwnd, 'w')
    # click_keys(target_hwnd, win32con.VK_CONTROL, win32con.VK_RETURN)
    # click_keys(target_hwnd, win32con.VK_CONTROL, win32con.VK_BACK)
