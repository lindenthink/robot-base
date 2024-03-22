import logging
from time import sleep

import win32gui

import common.my_mouse as my_mouse
import common.my_window as my_window
import weixin.wx_con as con


# 看广告并自动关闭
def watch_ad(hwnd, mode=my_window.MODE_BG):
    sleep(10)
    loc = my_window.wait_any_appear(hwnd=hwnd, template_paths=[con.BTN_AD_POP_CLOSE, con.ID_AD_FINISH], match_ratio=0.9,
                                    timeout=20, mode=mode)
    if loc is not None:
        if loc[1] > 200:
            logging.info(f'检测到弹出框，进行关闭')
            my_mouse.left_click(hwnd, loc)
            sleep(1)
            loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_AD_FINISH, match_ratio=0.9,
                                        mode=mode, timeout=20)
    my_mouse.left_click(hwnd, con.LOC_AD_CLOSE)
    sleep(1)


# 打开主窗口
def open_main():
    wnd = win32gui.FindWindow(con.WND_CLASS, con.TITLE)
    my_window.show(wnd)
    return wnd


# 最小化主窗口
def minimize_main():
    wnd = win32gui.FindWindow(con.WND_CLASS, con.TITLE)
    my_window.minimize(wnd)


# 枚举微信会话窗口
def enum_chat_wnds():
    result = my_window.enum_all(class_name=con.CHAT_CLASS)
    return result


# 打开指定小程序
def open_mini(mode=my_window.MODE_FG):
    wx_wnd = open_main()
    sleep(1)
    my_mouse.left_click(wx_wnd, con.LOC_MINI)
    sleep(1)
    # 新版入口弹出新窗口
    sub_wnd = win32gui.FindWindow(con.SUBWND_CLASS, con.TITLE)
    if sub_wnd:
        # 可能会导致失败：(5, 'SetForegroundWindow', '拒绝访问。')
        if mode == my_window.MODE_FG:
            my_window.force_focus(sub_wnd)
        loc = my_window.find_any_pic(hwnd=sub_wnd, template_paths=con.ID_MINI_GM_LIST, mode=mode)
        if loc is not None:
            my_mouse.left_click(sub_wnd, loc)
            sleep(1)
            my_window.close(sub_wnd)
            sleep(0.5)
    my_window.minimize(wx_wnd)
    sleep(1)


# 领取游戏圈礼包
def recv_moment_gift(mode=my_window.MODE_FG):
    sub_wnd = win32gui.FindWindow(con.SUBWND_CLASS, con.TITLE)
    if not sub_wnd:
        logging.info('未找到游戏圈窗口，等待下次重试')
        return False
    if mode == my_window.MODE_FG:
        my_window.force_focus(sub_wnd)
    loc = my_window.wait_appear(hwnd=sub_wnd, template_path=con.ID_MOMENT, mode=mode, timeout=10)
    if loc is None:
        logging.info('进入游戏圈页面超时，等待下次重试')
        return False
    x, y = loc
    loc = my_window.find_pic(hwnd=sub_wnd, template_path=con.BTN_MOMENT_RECV, mode=mode)
    if loc is None:
        logging.info('检测到已领取游戏圈奖励，本次忽略')
        my_window.close(sub_wnd)
        sleep(1)
        return True
    my_mouse.left_click(sub_wnd, (x, y + 75))
    sleep(2)
    loc = my_window.wait_appear(hwnd=sub_wnd, template_path=con.ID_MOMENT_SUCCESS, mode=mode, timeout=5)
    if loc is None:
        logging.info('领取超时或未领取成功，等待下次重试')
    my_window.close(sub_wnd)
    sleep(1)
    return loc is not None


# 删除微信聊天中分享的小程序内容
def delete_share(chat_wnd, loc):
    my_mouse.right_click(chat_wnd, loc)
    sleep(0.5)
    for i in range(0, 2):
        my_mouse.up_click(chat_wnd)
        sleep(0.1)
    my_mouse.enter_click(chat_wnd)
    sleep(0.5)
    confirm_wnd = win32gui.FindWindow(con.CONFIRM_CLASS, con.TITLE)
    if confirm_wnd:
        my_mouse.enter_click(confirm_wnd)
        sleep(0.5)
