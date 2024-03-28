# 获取窗口
import logging
import time
import gm.gm_con as con

from common import my_window, my_mouse, my_keyboard, my_util, my_cfg
from enum import Enum
import random

import win32con
import win32gui

import weixin.wx_func as wx_func
from datetime import datetime


def get_hwnd():
    meta = my_cfg.loadMeta()
    return my_window.find(meta['name'])


class EnterTaskResultEnum(Enum):
    success = 1
    fail = 0
    finished = 2


# 是否在主界面
def is_main_view(hwnd, mode=my_window.MODE_BG):
    if hwnd == 0 or my_window.find_pic(hwnd=hwnd, template_path=con.ID_MAIN_VIEW, mode=mode) is None:
        return False
    return True


# 检查遮挡，登陆/退出游历会触发
def check_notice(hwnd, mode=my_window.MODE_BG):
    if hwnd == 0:
        return
    if my_window.find_pic(hwnd=hwnd, template_path=con.ID_OFFLINE_INCOME, mode=mode) is not None:
        my_mouse.left_click(hwnd, (220, 120))
        logging.info('检测到离线收入弹框，进行关闭')
        time.sleep(1)

    # 点掉红点，否则每隔一段时间还会弹出公告
    if my_window.find_pic(hwnd=hwnd, template_path=con.ID_NOTICE, mode=mode) is not None:
        logging.info('检测到公告弹框，检查是否存在未读状态')
        loc_range = [(30, 160), (420, 200)]
        head_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_NOTICE_UNREAD, mode=mode,
                                             loc_range=loc_range)
        for head in head_list:
            my_mouse.left_click(hwnd, (head[0] - 10, head[1] + 10))
            time.sleep(1)
            loc_range = [(60, 215), (120, 600)]
            item_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_NOTICE_UNREAD2, mode=mode,
                                                 loc_range=loc_range)
            item_count = 0
            for item in item_list:
                my_mouse.left_click(hwnd, (item[0] - 10, item[1] + 10))
                time.sleep(1)
                item_count += 1
                logging.info(f'第{item_count}次处理未读公告')
        logging.info('检测处理完成，关闭公告弹框')
        my_mouse.left_click(hwnd, (220, 120))
        time.sleep(1)


# 检测下线：更新、顶号、连接断开
def check_offline(hwnd, mode=my_window.MODE_BG, interval=15):
    if hwnd == 0:
        return
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_OFFLINE_RETRY, mode=mode)
    if loc is not None:
        logging.info('检测到断开连接，将尝试刷新')
        refresh_login(hwnd, mode)
        return
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_OCCUPY_OFFLINE, mode=mode, do_capture=False)
    if loc is not None:
        logging.info(f'检测到被顶号，将于{interval}分钟后进行刷新')
        time.sleep(interval * 60)
        refresh_login(hwnd, mode)
        return
    loc = my_window.find_any_pic(hwnd=hwnd, mode=mode, do_capture=False,
                                 template_paths=[con.BTN_UPDATE_REENTRY, con.BTN_UPDATE_REENTRY2])
    if loc is not None:
        logging.info('检测到程序更新，将尝试重新登陆')
        # 更新需要关闭重启
        restart(mode)
        return


# 点击右下角退出
def rightdown_exit(hwnd):
    my_mouse.left_click(hwnd, con.LOC_GIFT_EXIT)
    time.sleep(2)


# 领取礼包
def rec_gift(hwnd, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, con.LOC_GIFT)
    time.sleep(1)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.BTN_GIFT_EXIT, mode=mode)
    if loc is None:
        logging.info('超时未进入礼包对话框，本次忽略处理')
        return False
    item_width = 70
    loc_first = (40, 775)
    for i in range(0, 8):
        if i >= 5:
            # 翻页
            my_mouse.left_drag(hwnd, (280, 775), (280 - item_width, 775))
            time.sleep(0.5)
            my_mouse.left_click(hwnd, (loc_first[0] + 4 * item_width, 775))
        else:
            my_mouse.left_click(hwnd, (loc_first[0] + i * item_width, 775))
        time.sleep(1)
        if i == 0:
            # 机缘
            my_mouse.left_click(hwnd, con.LOC_GIFT_JIYUAN_STEP1)
            time.sleep(0.5)
            my_mouse.left_click(hwnd, con.LOC_GIFT_JIYUAN_STEP2)
            time.sleep(0.5)
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_GONGFENG_RECEIVED, mode=mode)
            if loc is None:
                my_mouse.left_click(hwnd, con.LOC_GIFT_JIYUAN_STEP3)
                time.sleep(1)
                my_mouse.left_click(hwnd, con.LOC_GIFT_JIYUAN_STEP3)
                time.sleep(1)
            my_mouse.left_click(hwnd, con.LOC_GIFT_EXIT)
            time.sleep(1)
            logging.info('完成领取供奉奖励')
        elif i == 1:
            pass
        elif i == 2:
            loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_GIFT_DISPOSABLE, mode=mode)
            if loc is not None:
                my_mouse.left_click(hwnd, (150, 700))
                time.sleep(1)
            my_mouse.left_click(hwnd, (65, 640))
            time.sleep(1)
            my_mouse.left_click(hwnd, (150, 700))
            time.sleep(1)
            logging.info('完成领取每日特惠')
        elif i == 3:
            my_mouse.left_click(hwnd, con.LOC_GIFT_DAILY_0)
            time.sleep(1)
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_GIFT_DAILY_CHESS, mode=mode)
            if loc is not None:
                my_mouse.left_click(hwnd, (loc[0] + 50, loc[1] + 55))
                time.sleep(1)
            logging.info('完成领取和购买日礼包')
        elif i == 4:
            my_mouse.left_click(hwnd, con.LOC_GIFT_WEEKLY_0)
            time.sleep(0.5)
            my_mouse.left_click(hwnd, con.LOC_GIFT_WEEKLY_300)
            time.sleep(0.5)
            my_mouse.left_click(hwnd, con.LOC_GIFT_WEEKLY_500)
            time.sleep(0.5)
            logging.info('完成领取和购买周礼包')
        elif i == 5:
            for i in range(0, 2):
                loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_MCARD_REC, mode=mode)
                if loc is not None:
                    my_mouse.left_click(hwnd, loc)
                    time.sleep(2)
                    # 点击空白处
                    my_mouse.left_click(hwnd, (210, 700))
                    time.sleep(1)
            logging.info('完成领取月卡奖励')
        elif i == 6:
            pass
        elif i == 7:
            # 福礼阁
            first_loc = (135, 195)
            x_gap = 213
            y_gap = 123
            # 构造待播放按钮列表
            play_list = [first_loc]
            for i in range(2, 8):
                row = (i + 1) // 2
                col = i - (row - 1) * 2
                play_list.append((first_loc[0] + x_gap * (col - 1), first_loc[1] + y_gap * (row - 1)))
            i = 0
            while True:
                if i > 6:
                    break
                # logging.info(f'开始观看第{i + 1}个广告')
                next_play = play_list[i]
                finish_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_GIFT_AD_SELLOUT, mode=mode)
                has_play = False
                if len(finish_list) > 0:
                    for finish_play in finish_list:
                        if abs(next_play[0] - finish_play[0]) < 50 and abs(next_play[1] - finish_play[1]) < 50:
                            logging.info(f'第{i + 1}个广告已完成观看，本次忽略')
                            has_play = True
                            break
                if not has_play:
                    my_mouse.left_click(hwnd, next_play)
                    time.sleep(5)
                    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_GIFT_AD_PLAY, mode=mode)
                    if loc is not None:
                        logging.info('未进入广告界面，将进行重试')
                        time.sleep(1)
                        continue
                    wx_func.watch_ad(hwnd, mode=mode)
                    logging.info(f'第{i + 1}个广告观看完成')
                i += 1
            logging.info('完成领取福礼阁广告奖励')
    my_mouse.left_click(hwnd, con.LOC_GIFT_EXIT)
    time.sleep(1.5)
    return True


# 领取轮回棋局奖励
def chess_gift(hwnd, mode=my_window.MODE_BG, recv_range=None):
    if len(recv_range) == 0:
        return True
    todo_list = [con.CHESS_GIFTS[item] for item in recv_range]
    my_mouse.left_click(hwnd, con.LOC_CHESS)
    time.sleep(1)
    # 进入商店
    my_mouse.left_click(hwnd, (400, 520))
    time.sleep(1)
    # 进入魂殿
    loc = my_window.wait_click(hwnd=hwnd, mode=mode, template_path=con.ID_CHESS_ENTRY)
    if loc is None:
        my_mouse.left_click(hwnd, (105, 775))
        time.sleep(1)
    # 检测领取
    row_height = 190
    for i in range(0, 2):
        if i > 0:
            my_mouse.left_drag(hwnd, (40, 450), (40, 450 - row_height))
            time.sleep(1)
        while True:
            loc = my_window.find_any_pic(hwnd=hwnd, template_paths=todo_list, mode=mode)
            if loc is None:
                break
            my_mouse.move_to(hwnd, loc)
            my_mouse.left_click(hwnd, loc)
            time.sleep(1)
            my_mouse.left_click(hwnd, (225, 685))
            time.sleep(1.5)
    # 退出
    my_mouse.left_click(hwnd, (405, 770))
    time.sleep(1)
    my_mouse.left_click(hwnd, (405, 770))
    time.sleep(1)
    return True


# 招收弟子
def recruit(hwnd=0, mode=my_window.MODE_BG, accredit=True):
    enter_result = enter_task(hwnd=hwnd, no=7, mode=mode)
    if enter_result == EnterTaskResultEnum.fail:
        return False
    elif enter_result == EnterTaskResultEnum.finished:
        return True
    loc = enter_pointing(hwnd, mode)
    if loc is None:
        logging.info('招收入口超时未出现，忽略处理')
        return False
    red_count = 0
    for i in range(0, 2):
        # 首次已通过指示进入对话
        if i == 1:
            my_mouse.left_click(hwnd, loc)
            time.sleep(1)
        # 批量招收
        my_mouse.left_click(hwnd, (130, 560))
        time.sleep(1)
        loc2 = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_RECRUIT_VIEW, mode=mode)
        if loc2 is None:
            logging.info('超时未出现拜帖，忽略处理')
            return True
        while True:
            my_mouse.left_drag(hwnd, (300, 400), (140, 400))
            time.sleep(1)
            loc2 = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_RECRUIT, mode=mode)
            if loc2 is not None:
                break
        for j in range(0, 5 * (2 - i)):
            if accredit:
                # 自动派驻非红弟子
                loc2 = my_window.find_pic(hwnd=hwnd, template_path=con.ID_DISCIPLE_QICAI, mode=mode)
                if loc2 is None:
                    # 外门建筑有空位时没有快捷派驻
                    loc2 = my_window.find_click(hwnd=hwnd, template_path=con.ID_DISCIPLE_QUICK_STATION, mode=mode,
                                                do_capture=False)
                    if loc2 is not None:
                        continue
                red_count += 1
            my_mouse.left_click(hwnd, (330, 650))
            time.sleep(1)
        # 检测是否出现获得材料
        wait_acquire(hwnd=hwnd, mode=mode)
    if red_count > 0:
        logging.info(f'本次共获得{red_count}个红弟子，请自行处理')
    return True


# 日常-炼丹
def alchemy_daily(hwnd, mode, collect_pills=False):
    if not collect_pills:
        enter_result = enter_task(hwnd=hwnd, no=2, mode=mode)
        if enter_result == EnterTaskResultEnum.fail:
            return False
        elif enter_result == EnterTaskResultEnum.finished:
            return True
    loc = enter_pointing(hwnd, mode)
    if loc is None:
        logging.info('炼丹入口超时未出现，忽略处理')
        return False
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_ALCHEMY_FINISH, mode=mode)
    if loc is not None:
        logging.info('检测到已有炼制完成的丹药，本次直接领取不再进行炼丹')
        my_mouse.left_click(hwnd, loc)
        time.sleep(1.5)
        rightdown_exit(hwnd)
    elif my_window.find_pic(hwnd=hwnd, template_path=con.ID_ALCHEMY_EMPTY, mode=mode) is not None:
        # 检测是否分配炼丹弟子
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_NO_WORKER, mode=mode,
                                 loc_range=[(55, 675), (135, 760)])
        if loc is None:
            # 点击丹炉
            my_mouse.left_click(hwnd, (220, 450))
            time.sleep(1)
            # 选择药材
            my_mouse.left_click(hwnd, (235, 725))
            time.sleep(1)
            # 点击炼制
            my_mouse.left_click(hwnd, (270, 610))
            time.sleep(1)
            # 选择1次
            my_mouse.left_click(hwnd, (122, 462))
            time.sleep(1)
            # 确认
            my_mouse.left_click(hwnd, (225, 555))
            time.sleep(1)
            # 关炉
            my_mouse.left_drag(hwnd, (200, 490), (260, 490))
            time.sleep(1.5)
            # 点击互助
            my_mouse.left_click(hwnd, (240, 575))
            time.sleep(1)
            # 离开丹炉
            my_mouse.left_click(hwnd, (240, 575))
            time.sleep(1)
            logging.info('开始炼丹，可在3分钟后取消派驻弟子')
        else:
            logging.info('检测到未分配弟子，忽略处理')
    else:
        logging.info('检测到正在炼制丹药，忽略处理')
    # 点击退出
    rightdown_exit(hwnd)
    return True


# v2版本，加快突破速度
def breakthrough(hwnd, mode=my_window.MODE_BG, take_medicine=False):
    my_mouse.left_click(hwnd, con.LOC_DISCIPLE)
    time.sleep(1)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_DISCIPLE_VIEW, timeout=10, mode=mode)
    if loc is None:
        logging.info('进入弟子界面超时，忽略处理')
        return False
    check_medicine = True
    count = 1
    while True:
        loc_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_DISCIPLE_COMMA, mode=mode,
                                            loc_range=[(30, 440), (420, 715)], match_ratio=0.73)
        for loc1 in loc_list:
            my_mouse.left_click(hwnd, loc1)
            time.sleep(1)
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_DISCIPLE_LUNHUI, mode=mode)
            is_lunhui = loc is not None
            # 培养
            my_mouse.left_click(hwnd, (350, 205))
            time.sleep(1)
            # 修行
            if is_lunhui:
                my_mouse.left_click(hwnd, (190, 715))
            else:
                my_mouse.left_click(hwnd, (130, 715))
            time.sleep(1)
            # 检查是否被指导
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_GUIDED, mode=mode)
            if loc is not None:
                rightdown_exit(hwnd)
                continue
            # 检查突破
            loc = my_window.find_any_pic(hwnd=hwnd, template_paths=con.BTN_BREAKTHROUGH_TODO, mode=mode)
            if loc is not None:
                my_mouse.left_click(hwnd, (220, 495))
                time.sleep(1)
                # 只需要检查处理一次
                if check_medicine:
                    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_BREAKTHROUGH_NO_MEDICINE, mode=mode)
                    if take_medicine:
                        if loc is not None:
                            my_mouse.left_click(hwnd, (220, 455))
                            time.sleep(1)
                            my_mouse.left_click(hwnd, (200, 570))
                            time.sleep(1)
                    else:
                        if loc is None:
                            my_mouse.left_click(hwnd, (220, 455))
                            time.sleep(1)
                            my_mouse.left_click(hwnd, (200, 570))
                            time.sleep(0.5)
                            rightdown_exit(hwnd)
                    check_medicine = False
                my_mouse.left_click(hwnd, (220, 565))
                time.sleep(1)
                my_mouse.left_click(hwnd, (310, 515))
                time.sleep(1)
                loc = my_window.wait_any_appear(hwnd=hwnd, template_paths=con.ID_BREAKTHROUGH_RESULT, timeout=5,
                                                mode=mode)
                if loc is not None:
                    loc = my_window.find_any_pic(hwnd=hwnd, template_paths=con.ID_BREAKTHROUGH_RESULT_EXIT_TWICE,
                                                 mode=mode)
                    if loc is not None:
                        # 连续突破时不会出现成功/失败画面
                        rightdown_exit(hwnd)
                rightdown_exit(hwnd)
            rightdown_exit(hwnd)
        # 发现记名弟子，停止处理/早期没有记名弟子根据次数控制
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_DISCIPLE_TMP, mode=mode)
        if loc is not None or count >= 20:
            break
        # 继续处理下一批
        my_mouse.left_drag(hwnd, (400, 680), (400, 480))
        time.sleep(1)
        count += 1

    my_mouse.left_click(hwnd, (400, 765))
    time.sleep(1)
    return True


# 仙盟膜拜
def union_worship(hwnd, mode=my_window.MODE_BG):
    logging.info('开始执行自动膜拜')
    my_mouse.left_click(hwnd, con.LOC_UNION)
    time.sleep(1)
    my_window.wait_appear(hwnd=hwnd, template_path=con.ID_UNION_VIEW, mode=mode)
    time.sleep(1)
    my_mouse.left_click(hwnd, (225, 310))
    time.sleep(2)
    role_list = [(315, 385), (130, 510), (285, 705)]
    # 过滤未指定仙尊
    empty_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_UNION_WORSHIP_EMPTY, mode=mode)
    can_list = []
    for role in role_list:
        can = True
        for empty in empty_list:
            if abs(role[0] - empty[0]) < 80 and abs(role[1] - empty[1]) < 110:
                can = False
                break
        if can:
            can_list.append(role)
    if len(can_list) > 0:
        # 随机选择一个仙尊
        role = random.choice(can_list)
        my_mouse.left_click(hwnd, role)
        time.sleep(1)
        for i in range(0, 20):
            my_mouse.left_click(hwnd, (230, 640))
            time.sleep(1)
            wait_acquire(hwnd=hwnd, mode=mode)
    else:
        logging.info('三个仙尊均未指定，本次忽略处理')
    # 退出对话
    rightdown_exit(hwnd)
    # 退出膜拜
    rightdown_exit(hwnd)
    # 退出仙盟
    union_exit(hwnd, mode)
    logging.info('自动膜拜执行结束')


# 仙盟协助
def union_assist(hwnd, mode=my_window.MODE_BG, worship=True):
    loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_UNION_ASSIST, mode=mode)
    if loc is not None:
        if worship:
            union_worship(hwnd, mode)
        return True
    return False


# 仙盟红包
def union_hongbao(hwnd, mode=my_window.MODE_BG):
    loc = my_window.find_click(hwnd=hwnd, template_path=con.ID_UNION_HONGBAO, mode=mode)
    if loc is not None:
        rightdown_exit(hwnd)
        return True
    return False


# 进入游历
def enter_travel(hwnd=0, mode=None):
    my_mouse.left_click(hwnd, con.LOC_TRAVEL)
    time.sleep(2)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_TRAVEL_VIEW, timeout=10, mode=mode)
    if loc is None:
        logging.info('进入游历界面超时，忽略处理')
        return False
    time.sleep(0.5)


# 领取游历奖励，游历界面有时第一次点击没有反应需要增加判断处理
def travel(hwnd=0, count=1, mode=None):
    enter_travel(hwnd, mode)
    # 点击元宝盆
    my_mouse.left_click(hwnd, (65, 645))
    time.sleep(1.5)
    # 领取挂机
    my_mouse.left_click(hwnd, (320, 650))
    time.sleep(1)
    wait_acquire(hwnd=hwnd, mode=mode)
    # 点击元宝盆
    my_mouse.left_click(hwnd, (65, 645))
    time.sleep(1.5)
    # 机缘购买
    for i in range(0, count + 1):
        # 快速领取
        my_mouse.left_click(hwnd, (130, 665))
        time.sleep(1)
        if i == 0:
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_TRAVEL_FREE, mode=mode)
            if loc is None:
                logging.info('检测到免费资源已被领取，不再用机缘购买')
                rightdown_exit(hwnd)
                break
        # 领取
        my_mouse.left_click(hwnd, (220, 560))
        time.sleep(1)
        # 是否需要确认
        loc = my_window.wait_appear(hwnd=hwnd, template_path=con.BTN_CONFIRM, mode=mode)
        if loc is not None:
            my_mouse.left_click(hwnd, (310, 525))
            time.sleep(1)
            wait_acquire(hwnd=hwnd, mode=mode)
    rightdown_exit(hwnd)
    exit_travel(hwnd, mode)
    return True


def exit_travel(hwnd, mode):
    # 回城
    while True:
        rightdown_exit(hwnd)
        loc = my_window.wait_click(hwnd=hwnd, template_path=con.BTN_BACK_CITY, mode=mode)
        if loc is not None:
            # 防止点击无效增加一次检测
            time.sleep(1)
            my_window.wait_click(hwnd=hwnd, template_path=con.BTN_BACK_CITY, mode=mode)
            break
    backhome_check(hwnd, mode)


def backhome_check(hwnd, mode):
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_MAIN_VIEW, timeout=10, mode=mode)
    check_offline(hwnd)
    check_notice(hwnd)
    return loc is not None


# 分享
def share_game(hwnd, mode):
    enter_result = enter_task(hwnd=hwnd, no=8, mode=mode)
    if enter_result == EnterTaskResultEnum.fail:
        return False
    elif enter_result == EnterTaskResultEnum.finished:
        return True
    time.sleep(5)
    my_mouse.left_click_fg_ab(1160, 720)
    time.sleep(1)
    # 恢复任务列表到初始状态
    item_height = 59
    my_mouse.left_drag(hwnd, (290, 335), (290, 335 + 3 * item_height), num=20)
    rightdown_exit(hwnd)
    return True


# 悬赏
def reward(hwnd, mode=my_window.MODE_BG, stars=4, rebel_first=False, use_ticket=False, pay_refresh=False,
           only_rebel=False):
    my_mouse.left_click(hwnd, con.LOC_TASK)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_TASKLIST, mode=mode)
    if loc is None:
        logging.info('超时未进入任务列表界面，本次忽略处理')
        return False
    my_mouse.left_click(hwnd, (150, 665))
    time.sleep(1)
    loc_range = [(60, 255), (390, 550)]
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_COMMA, mode=mode, loc_range=loc_range)
    if loc is not None:
        logging.info('检测到已完成任务，进行领取')
        my_mouse.left_click(hwnd, (loc[0] - 20, loc[1] + 15))
        time.sleep(2)
        rightdown_exit(hwnd)

    search_pic = con.ID_REWARD_TODO if stars < 2 else con.ID_REWARD_STAR_LIST[stars - 2]
    while True:
        if not use_ticket:
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_TICKET, mode=mode)
            if loc is not None:
                logging.info('免费接取任务次数已用完，不再执行接取')
                break
        # 接取符合条件的任务
        todo_list = []
        if rebel_first:
            rebel_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_REWARD_REBEL, mode=mode,
                                                  loc_range=loc_range)
            todo_list += rebel_list
        # 接取符合星数的任务
        if not only_rebel:
            star_list = my_window.find_pic_multi(hwnd=hwnd, template_path=search_pic, mode=mode, loc_range=loc_range)
            todo_list += star_list

        # 检测并接取
        if len(todo_list) > 0:
            for todo in todo_list:
                begin_x = todo[0] - 30
                begin_y = todo[1] - 10
                loc_range_todo = [(begin_x, begin_y), (begin_x + 80, begin_y + 140)]
                todo_pic = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_TODO, mode=mode,
                                              loc_range=loc_range_todo)
                if todo_pic is None:
                    continue
                # 点击任务
                my_mouse.left_click(hwnd, todo)
                time.sleep(1)
                # 一键委派
                my_mouse.left_click(hwnd, (115, 550))
                time.sleep(1)
                # 检查是否委派成功
                loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_NO_WORKER, mode=mode)
                if loc is not None:
                    logging.info('未能委派成功，忽略处理')
                    rightdown_exit(hwnd)
                    continue
                # 接取
                my_mouse.left_click(hwnd, (345, 550))
                time.sleep(1)
                # 每次接取后增加校验免费次数
                if not use_ticket:
                    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_TICKET, mode=mode)
                    if loc is not None:
                        logging.info('免费接取任务次数已用完，不再执行接取')
                        break
        else:
            logging.info(f'本轮未检测到满足最低{stars}星的任务')

        # 检测任务是否接满，接满时不可刷新
        loc = my_window.find_any_pic(hwnd=hwnd, template_paths=[con.ID_REWARD_TODO, con.ID_REWARD_EMPTY], mode=mode)
        if loc is None:
            logging.info('检测到已接满6个任务，本次不再处理')
            break

        if not pay_refresh:
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_REFRESH_FREE, mode=mode)
            if loc is None:
                logging.info('免费刷新冷却中，等待下次处理')
                break
        # 刷新
        my_mouse.left_click(hwnd, (220, 590))
        time.sleep(1)
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_CONFIRM, mode=mode)
        if loc is not None:
            logging.info('刷新时有高星任务提示，等待下次尝试重新接取')
            rightdown_exit(hwnd)
            break
    # 互助
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_REWARD_ASSIST, mode=mode)
    if loc is not None:
        my_mouse.left_click(hwnd, (320, 585))
        time.sleep(0.5)
    rightdown_exit(hwnd)
    return True


# 藏经阁研习
def study(hwnd, mode, collect_pills=False):
    enter_result = enter_task(hwnd=hwnd, no=3, mode=mode)
    if enter_result == EnterTaskResultEnum.fail:
        return False
    elif enter_result == EnterTaskResultEnum.finished:
        # 先判断是否有完成&空闲炼丹标识并进行领取，否则研习标识不会展示
        if collect_pills:
            for i in range(0, 2):
                loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_ALCHEMY_PROMPT, mode=mode)
                if loc is not None:
                    logging.info('检测到存在炼丹按钮，处理完成后再继续执行藏经阁研习')
                    my_mouse.left_click(hwnd, loc)
                    time.sleep(1)
                    alchemy_daily(hwnd, mode, collect_pills=True)
                else:
                    break
        # 判断是否存在研习按钮
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_STUDY, mode=mode)
        if loc is not None:
            my_mouse.left_click(hwnd, loc)
            time.sleep(1)
        else:
            logging.info('研习按钮不存在，等待下次处理')
            return False

    loc = enter_pointing(hwnd, mode, x_offset=40)
    if loc is None:
        logging.info('寻找藏经阁超时，忽略处理')
        return False
    my_mouse.left_click(hwnd, loc)
    time.sleep(2)
    my_mouse.left_click(hwnd, (220, 425))
    time.sleep(1)
    my_mouse.left_click(hwnd, (220, 735))
    time.sleep(2.5)
    my_mouse.left_click(hwnd, (220, 560))
    time.sleep(0.5)
    my_mouse.left_click(hwnd, (220, 560))
    time.sleep(0.5)
    rightdown_exit(hwnd)
    return True


# 心事,弟子经过的地方尽量不要放遮挡视线的建筑
def click_thinking(hwnd, mode=my_window.MODE_BG):
    check_wrong_click(hwnd, mode)
    loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_THINKING, mode=mode)
    if loc is None:
        return False
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.BTN_THINKING_2, timeout=20, mode=mode,
                                loc_range=[(20, 175), (440, 575)])
    if loc is None:
        logging.info('寻找心事弟子超时，忽略处理')
        return False
    my_mouse.left_click(hwnd, loc)
    time.sleep(1)
    # 额外增加几次尝试确认
    if not my_util.retry(is_talking, 3, hwnd=hwnd, mode=mode):
        logging.info('检测到未能成功进入心事对话，进行重试')
        click_thinking(hwnd)
        return False
    count = 0
    while True:
        # 点击第一个选项位置
        my_mouse.left_click(hwnd, (150, 585))
        time.sleep(0.5)
        count += 1
        if count < 3:
            continue
        check_challenge(hwnd, mode)
        if is_talking(hwnd, mode):
            continue
        if not check_wrong_click(hwnd, mode):
            return True


# 访客，间隔3分钟
def click_visitor(hwnd, mode=my_window.MODE_BG):
    loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_VISITOR, mode=mode)
    if loc is None:
        return False
    loc = my_window.wait_click(hwnd=hwnd, template_path=con.BTN_VISITOR_2, timeout=10, mode=mode,
                               loc_range=[(210, 300), (270, 350)])
    if loc is None:
        logging.info('寻找访客超时，忽略处理')
        return False
    count = 0
    while True:
        my_mouse.left_click(hwnd, (150, 585))
        time.sleep(0.5)
        count += 1
        if count < 4:
            continue
        if not check_challenge(hwnd, mode):
            loc = my_window.find_any_pic(hwnd=hwnd, template_paths=con.BTN_VISITOR_OPTIONS, mode=mode)
            if loc is not None:
                my_mouse.left_click(hwnd, loc)
                time.sleep(1)
                loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_CONFIRM, mode=mode)
        if not is_talking(hwnd, mode):
            check_notice(hwnd, mode)
            break
    return True


# 检查挑战，月灵风影访客以及切磋心事
def check_challenge(hwnd, mode=None):
    loc = my_window.find_click(hwnd=hwnd, template_path=con.BTN_VISITOR_FIGHT, mode=mode)
    if loc is not None:
        loc = my_window.wait_click(hwnd, mode=mode, template_path=con.ID_BOSS_EXIT)
        loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_EXIT_HINT, timeout=90, mode=mode)
        if loc is None:
            logging.info('等待挑战结束超时，忽略处理')
            return False
        rightdown_exit(hwnd)
        while True:
            if not is_talking(hwnd, mode):
                time.sleep(1)
            else:
                return True
    return False


# 判断是否在对话
def is_talking(hwnd, mode):
    loc = my_window.find_any_pic(hwnd=hwnd, template_paths=con.ID_TALKING, mode=mode)
    return loc is not None


# 判断处理误点招募、建筑等
def check_wrong_click(hwnd, mode):
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_BUILDING_DETAIL, mode=mode)
    if loc is not None:
        rightdown_exit(hwnd)
        logging.info('检测到误点到建筑，自动退出')
        return True
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_NO_ENTRY, mode=mode)
    if loc is not None:
        rightdown_exit(hwnd)
        logging.info('检测到无法通行提示，自动退出')
        return True
    return False


# 运行前检查
def readiness_check(hwnd, mode):
    if hwnd == 0:
        logging.info('检测失败，未找到游戏窗口')
        return False
    w, h = my_window.get_size(hwnd)
    if w < 200:
        logging.info('检测到目标窗口被最小化，将自动恢复')
        my_window.restore(hwnd)
        w, h = my_window.get_size(hwnd)
    if w != 450 or h != 844:
        logging.info(f'检测到目标窗口大小为{w}*{h}，自动调整为450*844')
        my_window.resize(hwnd, 450, 844)
    return check_chat(hwnd, mode)


# 检测聊天气泡框位置
def check_chat(hwnd, mode):
    if hwnd == 0:
        logging.info('检测失败，未找到目标窗口')
        return False
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_CHAT, mode=mode)
    if loc is None:
        logging.info('检测失败，请保证聊天气泡不被遮挡')
        return False
    else:
        from_x, from_y = loc
        if from_x < 350 or from_y > 150:
            logging.info('检测到聊天对话框位置可能遮挡部分图标，将自动调整到右上角')
            my_mouse.left_drag(hwnd, (from_x + 5, from_y + 5), (380, 70))
            time.sleep(1)
    return True


# 领取锁妖塔灵石
def tower_gift(hwnd, mode, sweep=True):
    enter_result = enter_task(hwnd=hwnd, no=10, mode=mode)
    if enter_result == EnterTaskResultEnum.fail:
        return False
    elif enter_result == EnterTaskResultEnum.finished:
        return True
    loc = enter_pointing(hwnd, mode=mode, x_offset=0, y_offset=80)
    if loc is None:
        logging.info('寻找七曜塔超时，忽略处理')
        return False
    time.sleep(1)
    my_mouse.left_click(hwnd, (200, 320))
    time.sleep(1)
    my_mouse.left_click(hwnd, (370, 395))
    time.sleep(2)
    rightdown_exit(hwnd)
    if sweep:
        page = 1
        while True:
            loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_COMMA, mode=mode)
            # 限定检测叹号的范围
            found = loc is not None and loc[0] < 405 and loc[1] < 655
            if not found:
                if page < 3:
                    my_mouse.left_drag(hwnd, (210, 640), (210, 180), num=40)
                    time.sleep(0.5)
                    page += 1
                    continue
                else:
                    break
            # 根据感叹号入塔
            my_mouse.left_click(hwnd, (loc[0] - 200, loc[1] + 85))
            time.sleep(1)
            # 扫荡
            my_mouse.left_click(hwnd, (140, 645))
            time.sleep(1)
            while True:
                # 确认扫荡
                my_mouse.left_click(hwnd, (220, 505))
                time.sleep(0.5)
                loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_TOWER_GIFT_FREE, mode=mode)
                if loc is None:
                    rightdown_exit(hwnd)
                    rightdown_exit(hwnd)
                    break
    rightdown_exit(hwnd)
    return True


# 斗技
def contend(hwnd=0, count=3, is_triple=True, fight_3rd=True, right_exit=False, mode=my_window.MODE_BG, caller=None):
    if not my_util.in_progress('08:00', '22:00'):
        logging.info('未在活动时间范围内，忽略处理')
        return
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_DOUJI_HOME, mode=mode)
    if loc is None:
        logging.info('未处于斗技界面，忽略处理')
        return

    for i in range(0, count):
        if caller is not None:
            if caller.isStop:
                return
            logging.info(f'开始执行第{i + 1}次斗技')
        # 增加过程中时间校验
        if not my_util.in_progress('08:00', '22:00'):
            logging.info('未在活动时间范围内，忽略处理')
            return
        # 挑战
        my_mouse.left_click(hwnd, (220, 705))
        time.sleep(1)
        if fight_3rd:
            my_mouse.left_click(hwnd, (350, 510))
        else:
            my_mouse.left_click(hwnd, (350, 365))
        time.sleep(2)
        # 检测是否进入战斗画面
        loc = my_window.wait_appear(hwnd=hwnd, template_path=con.BTN_RETREAT, timeout=20, mode=mode)
        if loc is None:
            logging.info('等待进入战斗画面超时，忽略处理')
            continue
        time.sleep(1)
        if right_exit:
            my_mouse.left_click(hwnd, loc)
            time.sleep(1.5)
            my_mouse.left_click(hwnd, (310, 535))
            time.sleep(1)
        elif is_triple:
            check_triple(hwnd, mode)
        loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_DOUJI_FINISHED, timeout=120, mode=mode)
        my_mouse.left_click(hwnd, (220, 650))
        time.sleep(2)

# 文本输入
# 无法实现组合按键
# 需要注意当存在换行时END只能定位到当前行末尾，需要逐行删除处理
def input_text(hwnd, text):
    my_mouse.left_click(hwnd, con.LOC_TEXT)
    time.sleep(0.2)
    my_keyboard.click_keys(hwnd, win32con.VK_CONTROL, win32con.VK_END)
    for i in range(120):
        win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_BACK, 0)
        win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_BACK, 0)
    for ch in text:
        win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(ch), 0)
    my_mouse.left_click(hwnd, con.LOC_TEXT_FINISH)
    time.sleep(0.5)


# 建筑/炼丹等看广告
def watch_ad(hwnd, mode=my_window.MODE_BG, use_timesand=True, caller=None):
    while True:
        if caller.isStop:
            break
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_TIME_SAND, match_ratio=0.7, mode=mode)
        if loc is not None:
            if not use_timesand:
                break
            my_mouse.left_click(hwnd, con.LOC_AD_CONFIRM)
            time.sleep(0.2)
            continue
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_AD_FREE, mode=mode)
        if loc is None:
            logging.info('已完成观看，本次任务完成')
            break
        else:
            my_mouse.left_click(hwnd, con.LOC_AD_CONFIRM)
            wx_func.watch_ad(hwnd)


def close():
    hwnd = get_hwnd()
    if hwnd != 0:
        logging.info('开始关闭游戏')
        my_window.close(hwnd)
        time.sleep(1)


# 重新登陆，从微信启动
def restart(mode=my_window.MODE_BG):
    while True:
        close()
        logging.info('准备启动游戏，完成启动前请勿操作鼠标和键盘！')
        time.sleep(1)
        wx_func.open_mini(mode)
        my_util.retry(get_hwnd, 10)
        hwnd = get_hwnd()
        if hwnd > 0:
            break
        logging.info('超时未发现游戏窗口，即将重试...')
        time.sleep(1)
    my_window.move_lt(hwnd)
    time.sleep(0.5)
    my_window.show(hwnd)
    time.sleep(0.5)
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_UPDATE_RETRY, mode=mode)
    if loc is not None:
        logging.info('检测到未更新完成，10分钟后进行重试')
        time.sleep(10 * 60)
        restart(mode)
        return
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_MAIN_VIEW, timeout=30, mode=mode)
    if loc is None:
        logging.info('进入主界面超时，重新登陆')
        restart(mode)
        return
    check_notice(hwnd)
    readiness_check(hwnd, mode)
    # 等待加载资源
    time.sleep(3)
    return True


# 刷新登录，不用从微信启动游戏
def refresh_login(hwnd=0, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, (350, 25))
    time.sleep(1)
    my_mouse.left_click(hwnd, (215, 270))
    time.sleep(2)

    my_util.retry(get_hwnd, 10)
    hwnd = get_hwnd()
    if not hwnd:
        logging.info('超时未获取到游戏窗口，重新打开...')
        restart(mode)
        return True
    my_window.move_lt(hwnd)
    time.sleep(0.5)
    my_window.show(hwnd)
    time.sleep(0.5)
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.BTN_UPDATE_RETRY, mode=mode)
    if loc is not None:
        logging.info('检测到未更新完成，10分钟后重试刷新登录...')
        time.sleep(10 * 60)
        refresh_login(hwnd, mode)
        return
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_MAIN_VIEW, timeout=30, mode=mode)
    if loc is None:
        logging.info('进入主界面超时，重新刷新登陆...')
        refresh_login(hwnd, mode)
        return
    check_notice(hwnd)
    readiness_check(hwnd, mode)
    # 等待加载资源
    time.sleep(3)
    return True


# 妖王
def demon(hwnd=0, mode=my_window.MODE_BG, is_triple=True):
    wxs = wx_func.enum_chat_wnds()
    for wx in wxs.keys():
        loc = my_window.find_pic(hwnd=wx, template_path=con.ID_DEMON_WX, mode=my_window.MODE_BG, match_ratio=0.9)
        if loc is None:
            continue
        if not check_share(wx, loc, 55):
            continue
        my_mouse.left_click(wx, loc)
        time.sleep(1)
        target_loc = loc
        logging.info(f'对话框<{wxs[wx]}>存在妖王，开始执行')
        loc = my_window.wait_appear(hwnd=hwnd, mode=mode, template_path=con.BTN_EXIT,
                                    loc_range=[(380, 760), (440, 820)])

        if loc is None:
            delete_share(hwnd, wx, target_loc)
            loc = my_window.find_pic(hwnd=hwnd, mode=mode, template_path=con.ID_DEMON_NULL)
            if loc is not None:
                logging.info('检测到妖王已消失提示，忽略处理')
                my_mouse.left_click(hwnd, (220, 525))
                time.sleep(1)
                continue
            else:
                logging.info('等待进入妖王超时，忽略处理')
                continue
        my_mouse.left_click(hwnd, (220, 790))
        time.sleep(0.5)
        my_mouse.left_click(hwnd, (220, 635))
        time.sleep(0.5)
        delete_share(hwnd, wx, target_loc)
        result = check_fight(hwnd, mode, is_triple=is_triple, right_exist=False)
        rightdown_exit(hwnd)
        # 未成功继续检测其他窗口
        if result:
            return True
    return False


# 任务-妖窟
def task_boss(hwnd=0, mode=my_window.MODE_BG, qualities=None, types=None):
    template_paths = _get_template_paths(qualities, types)
    return boss(hwnd, mode, template_paths, caller=None)


# 独立模块-妖窟
def single_boss(hwnd=0, mode=my_window.MODE_BG, caller=None, count=3, qualities=None, types=None,
                use_money=False, farm=False, farm_interval=5):
    if use_money:
        money_farm(hwnd, mode, caller)
        return
    template_paths = _get_template_paths(qualities, types)
    i = 1
    next_time = my_util.addMinutes(datetime.now(), farm_interval)
    while True:
        if i <= count:
            result = boss(hwnd, mode, template_paths, True, caller=caller)
            if result:
                logging.info(f'执行完成，已成功上车{i}次')
                i += 1
        if farm:
            now = datetime.now()
            if now > next_time:
                logging.info(f'开始执行刷材料...')
                farm = boss_farm(hwnd, mode, caller=caller)
                next_time = my_util.addMinutes(now, farm_interval)
                logging.info(f'刷材料执行完成，下次执行时间：{my_util.fmtDateTime(next_time)}')
        if caller.isStop:
            break


def _get_template_paths(qualities=None, types=None):
    result = list()
    for qt in qualities:
        for tp in types:
            template_name = f'boss_{con.BOSS_TYPES[tp]}_{con.BOSS_QUALITIES[qt]}'
            result.append(con.join(template_name))
    return result


# 妖窟BOSS
def boss(hwnd=0, mode=my_window.MODE_BG, template_paths=None, use_ticket=False, caller=None):
    wxs = wx_func.enum_chat_wnds()
    for wx in wxs.keys():
        loc = my_window.find_any_pic(hwnd=wx, mode=my_window.MODE_BG, template_paths=template_paths, match_ratio=0.97)
        if loc is None:
            continue
        if not check_share(wx, loc):
            continue
        target_loc = loc
        logging.info(f'微信群聊<{wxs[wx]}>存在目标BOSS，开始执行上车')
        my_mouse.left_click(wx, (loc[0] + 100, loc[1] + 100))
        time.sleep(0.5)
        # 先判断是否进入BOSS界面
        loc = my_window.wait_appear(hwnd=hwnd, mode=mode, template_path=con.BTN_EXIT,
                                    loc_range=[(380, 760), (440, 820)])
        if loc is None:
            loc = my_window.find_pic(hwnd=hwnd, mode=mode, template_path=con.ID_BOSS_NONE)
            if loc is not None:
                logging.info('检测到BOSS不存在提示，忽略处理')
                my_mouse.left_click(hwnd, (220, 525))
                time.sleep(1)
                delete_share(hwnd, wx, target_loc)
                continue
            else:
                logging.info('等待进入妖窟超时，忽略处理')
                continue
        # 检测是否使用道具
        if not use_ticket:
            time.sleep(0.5)
            loc = my_window.find_pic(hwnd=hwnd, mode=mode, template_path=con.ID_BOSS_TICKET)
            if loc is not None:
                logging.info('检测到免费次数已用完且不使用镇魔令，忽略处理')
                rightdown_exit(hwnd)
                return True
        my_mouse.left_click(hwnd, (120, 790))
        time.sleep(0.5)
        my_mouse.left_click(hwnd, (225, 640))
        time.sleep(1)
        # 上车即删除
        delete_share(hwnd, wx, target_loc)
        result = check_fight(hwnd, mode, right_exist=True)
        # 回到妖窟入口
        rightdown_exit(hwnd)
        rightdown_exit(hwnd)
        check_notice(hwnd)
        # 未成功继续检测其他窗口
        if result:
            return True
    return False


# 删除微信分享内容
def delete_share(hwnd, wx, loc):
    # 需要将其他窗口最小化，否则将导致删除失效
    my_window.minimize(hwnd)
    my_window.show(wx)
    time.sleep(0.5)
    wx_func.delete_share(wx, loc)
    time.sleep(0.5)
    my_window.show(hwnd)


# 检查战斗，妖窟和妖王
def check_fight(hwnd, mode, right_exist=False, is_triple=False):
    loc = my_window.wait_appear(hwnd, mode=mode, template_path=con.ID_BOSS_EXIT, timeout=10,
                                loc_range=[(380, 600), (440, 680)])
    if loc is None:
        logging.info('检测到超时未进入战斗，忽略处理')
        return False
    if right_exist:
        my_mouse.left_click(hwnd, loc)
        time.sleep(1)
        # 可能存在点击无效问题，此处暂时通过多尝试一次解决
        for i in range(0, 2):
            my_mouse.left_click(hwnd, (310, 535))
            time.sleep(0.5)
    elif is_triple:
        check_triple(hwnd, mode)
    loc = my_window.wait_click(hwnd=hwnd, template_path=con.ID_EXIT_HINT, timeout=300, mode=mode)
    if loc is None:
        logging.info('等待挑战结束超时，忽略处理')
        return False
    return True


# 机缘刷材料，进入boss界面后开启
def money_farm(hwnd, mode=None, caller=None):
    count = 1
    while True:
        if caller is not None and caller.isStop:
            break
        loc = my_window.find_pic(hwnd, mode, template_path=con.ID_BOSS_JIANGCHI)
        if loc is None:
            logging.info('当前不处于妖窟模式界面，忽略处理')
            return
        loc = my_window.find_pic(hwnd, mode, template_path=con.ID_BOSS_CHOUJIANG, do_capture=False)
        if loc is not None:
            logging.info('已进入抽奖环节，停止处理')
            rightdown_exit(hwnd)
            return
        logging.info(f'开始执行第{count}次机缘刷材料')
        loc_taofa = my_window.find_any_pic(hwnd=hwnd, mode=mode, template_paths=con.ID_BOSS_TAOFA_LIST,
                                           do_capture=False)
        if loc_taofa is None:
            # 需要使用机缘
            my_mouse.left_click(hwnd, (220, 790))
            time.sleep(1.5)
            # 免费立即完成
            loc = my_window.find_click(hwnd, mode, template_path=con.ID_RIGHT_FINISH, match_ratio=0.9)
            if loc is None:
                my_mouse.left_click(hwnd, (225, 525))
                time.sleep(1.5)
                # 确认使用机缘
                my_mouse.left_click(hwnd, (310, 520))
                time.sleep(1.5)
        my_mouse.left_click(hwnd, (220, 790))
        time.sleep(1.5)
        # 确认讨伐
        my_mouse.left_click(hwnd, (225, 635))
        time.sleep(1)
        check_fight(hwnd, mode, right_exist=True)
        count += 1


# 刷材料
def boss_farm(hwnd, mode=None, caller=None):
    logging.info('开始搜集妖窟BOSS材料')
    # 检查所在面板
    loc = my_window.find_pic(hwnd, mode, template_path=con.ID_BOSS_YAOKU)
    if loc is None:
        if is_main_view(hwnd, mode):
            enter_travel(hwnd, mode)
            my_mouse.left_click(hwnd, (75, 95))
            time.sleep(2)
        else:
            logging.info('当前不处于主页/妖窟页，忽略处理')
            return False
    page_size = 6
    line_height = 70
    count = 1
    first_btn_loc = (330, 285)
    while True:
        loc = my_window.find_click(hwnd, mode, template_path=con.ID_BOSS_XIEZHAN)
        if loc is None:
            logging.info('未发现协战入口，停止处理')
            break
        if count > page_size:
            my_mouse.left_drag(hwnd, (200, 550), (150, 550 - line_height))
            interval = (page_size - 1) * line_height
        else:
            interval = (count - 1) * line_height
        btn_loc = [first_btn_loc[0], first_btn_loc[1] + interval]
        btn_loc = my_window.find_click(hwnd, mode, template_path=con.ID_BOSS_XIEZHAN_2,
                                       loc_range=[(btn_loc[0] - 35, btn_loc[1] - 20),
                                                  (btn_loc[0] + 35, btn_loc[1] + 20)])
        if btn_loc is None:
            rightdown_exit(hwnd)
            break
        loc_taofa = my_window.find_any_pic(hwnd=hwnd, mode=mode, template_paths=con.ID_BOSS_TAOFA_LIST)
        if loc_taofa is not None:
            my_mouse.left_click(hwnd, loc_taofa)
            time.sleep(1)
            # 确认讨伐
            my_mouse.left_click(hwnd, (225, 635))
            time.sleep(1)
            check_fight(hwnd, mode, right_exist=True)
        rightdown_exit(hwnd)
        count += 1
    exit_travel(hwnd, mode)
    logging.info('完成搜集妖窟BOSS材料')
    return True


# 镇妖涧
def zhenyaojian(hwnd, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, con.LOC_UNION)
    time.sleep(2)
    my_mouse.left_click(hwnd, (25, 180))
    time.sleep(1)

    # 挑战
    my_mouse.left_click(hwnd, (300, 790))
    time.sleep(1)
    # 检查剩余次数
    loc = my_window.find_pic(hwnd, template_path=con.ID_ZHENYAO_NONE, mode=mode)
    if loc is not None:
        logging.info('剩余次数为0，本次忽略处理')
        zhenyaojian_exit(hwnd, mode)
        return True
    # 确认
    my_mouse.left_click(hwnd, (220, 635))
    time.sleep(2)
    result = True
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_DEMON_FIGHT, timeout=10, mode=mode)
    if loc is None:
        logging.info('进入镇妖涧战斗界面超时，等待下次重试')
        result = False
    check_triple(hwnd, mode)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_EXIT_HINT, timeout=120, mode=mode)
    if loc is None:
        logging.info('等待结束超时，忽略处理镇妖涧BOSS')
        result = False
    # 两次退出
    rightdown_exit(hwnd)
    zhenyaojian_exit(hwnd, mode)
    return result


# 从镇妖涧对话框退出
def zhenyaojian_exit(hwnd, mode=my_window.MODE_BG):
    loc = my_window.wait_click(hwnd=hwnd, template_path=con.BTN_EXIT, timeout=10, mode=mode)
    if loc is None:
        logging.info('等待退出按钮出现超时，忽略处理镇妖涧BOSS')
        return False
    time.sleep(1)
    union_exit(hwnd, mode)


# 从仙盟退出
def union_exit(hwnd, mode=my_window.MODE_BG):
    for i in range(1, 10):
        my_mouse.left_click(get_hwnd(), (400, 765))
        time.sleep(1)
        in_main = backhome_check(hwnd, mode)
        if in_main:
            break


# 铸造
def foundry(hwnd, level=4, mode=my_window.MODE_BG, caller=None, dec_round=3, dec_qlty=2):
    loc = my_window.find_pic(hwnd, template_path=con.ID_ZHULIAN_VIEW, mode=mode)
    if loc is None:
        logging.info('未进入铸炼界面，本次忽略处理')
        return
    loc = my_window.find_pic_multi(hwnd, template_path=con.ID_ZHULIAN_NO_WORKER, mode=mode)
    if len(loc) == 2:
        logging.info('检测到未指派弟子，本次忽略处理')
        return
    # 获取等级对应坐标
    l_x, l_y = con.LOC_ZHULIAN_LEVEL_8
    l_x = max(65, l_x - 60 * (8 - level))
    drop_count = 0 if level > 2 else 3 - level
    # 按类型循环
    types = ['', con.LOC_ZHULIAN_TYPE_2, con.LOC_ZHULIAN_TYPE_3]
    count = 0
    for tp in types:
        foundry_select(hwnd, tp=tp, drop_count=drop_count, loc=(l_x, l_y))
        while True:
            if caller is not None:
                if caller.isStop:
                    return
            time.sleep(1)
            loc = my_window.find_pic(hwnd, template_path=con.ID_ZHULIAN_EMPTY, mode=mode)
            if loc is not None:
                # 材料为空，准备换类型
                my_mouse.left_click(hwnd, (200, 540))
                time.sleep(1)
                break
            logging.info(f'开始第{count + 1}轮装备铸造')
            my_mouse.left_click(hwnd, con.LOC_ZHULIAN_2)
            time.sleep(1)
            my_mouse.left_click(hwnd, con.LOC_ZHULIAN_CONFIRM)
            time.sleep(1)
            loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_ZHULIAN_ING, mode=mode)
            if loc is None:
                logging.info('超时未进入铸炼中界面，本次忽略')
                continue
            # 快速铸造
            loc = my_window.wait_click(hwnd=hwnd, template_path=con.BTN_QUICK_ZHULIAN, mode=mode)
            wait_acquire(hwnd=hwnd, mode=mode, timeout=30)
            count += 1
            # 分解，防止背包中超过1000件无法继续铸造
            if count % dec_round == 0:
                logging.info('开始执行装备分解')
                my_mouse.left_click(hwnd, (200, 540))
                time.sleep(1)
                foundry_dec(hwnd, level=level, dec_qlty=dec_qlty)
                foundry_select(hwnd, tp=tp, drop_count=drop_count, loc=(l_x, l_y))

    if count != 0 and count % 3 != 0:
        logging.info('铸造材料已用完，开始执行结束前分解')
        foundry_dec(hwnd, level=level, dec_qlty=dec_qlty)


def wait_acquire(hwnd=None, mode=None, timeout=6):
    id_loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_ACQUIRE, timeout=timeout, mode=mode)
    if id_loc is not None:
        time.sleep(1)
        rightdown_exit(hwnd)


# 铸炼-选择等级
def foundry_select(hwnd, tp=None, drop_count=0, loc=(0, 0)):
    l_x, l_y = loc
    my_mouse.left_click(hwnd, con.LOC_ZHULIAN_1)
    time.sleep(1)
    for i in range(0, drop_count):
        my_mouse.left_drag(hwnd, (125, l_y), (185, l_y), 20)
    my_mouse.left_click(hwnd, (l_x, l_y))
    time.sleep(1)
    if tp != '':
        my_mouse.left_click(hwnd, tp)
        time.sleep(1)
    my_mouse.left_click(hwnd, con.LOC_ZHULIAN_TYPE_SELECT)


# 铸炼-分解
def foundry_dec(hwnd, dec_qlty=2, level=4):
    my_mouse.left_click(hwnd, (215, 770))
    time.sleep(1)
    my_mouse.left_click(hwnd, (120, 655))
    time.sleep(1)
    # 选择品质
    baseX = 140
    baseY = 395
    for i in range(0, min(3, dec_qlty)):
        if i == 0:
            continue
        my_mouse.left_click(hwnd, (baseX + i * 90, baseY))
        time.sleep(0.5)
    if dec_qlty > 3:
        for i in range(0, dec_qlty - 3):
            my_mouse.left_click(hwnd, (baseX + i * 90, baseY + 40))
            time.sleep(0.5)

    # 选择境界，和等级相同
    baseY = 515
    for i in range(0, min(3, level)):
        if i == 0:
            continue
        my_mouse.left_click(hwnd, (baseX + i * 90, baseY))
        time.sleep(0.5)
    if level > 3:
        for i in range(0, min(3, level - 3)):
            my_mouse.left_click(hwnd, (baseX + i * 90, baseY + 40))
            time.sleep(0.5)
    if level > 6:
        for i in range(0, level - 6):
            my_mouse.left_click(hwnd, (baseX + i * 90, baseY + 40 * 2))
            time.sleep(0.5)

    my_mouse.left_click(hwnd, (225, 650))
    time.sleep(1)
    my_mouse.left_click(hwnd, (325, 655))
    time.sleep(1)
    my_mouse.left_click(hwnd, (340, 615))
    time.sleep(1)
    for i in range(0, 2):
        my_mouse.left_click(hwnd, (405, 810))
        time.sleep(1)


# 检查设置三倍速
def check_triple(hwnd, mode):
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_SPEED, mode=mode)
    if loc is None:
        return
    for i in range(0, 2):
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_TRIPLE, mode=mode)
        if loc is not None:
            break
        my_mouse.left_click(hwnd, (415, 495))
        time.sleep(0.5)


# 根据指示箭头点击建筑
def enter_pointing(hwnd, mode=my_window.MODE_BG, x_offset=10, y_offset=120):
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_POINTING, mode=mode, timeout=10)
    if loc is None:
        return loc
    base_x, base_y = loc
    target_x = base_x + x_offset
    target_y = base_y + y_offset
    my_mouse.left_click(hwnd, (target_x, target_y))
    time.sleep(1)
    return target_x, target_y


# 领取游戏圈礼包
def recv_moment_gift(hwnd, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, (45, 110))
    time.sleep(1.5)
    my_mouse.left_click(hwnd, (80, 160))
    time.sleep(1)
    my_mouse.left_click(hwnd, (230, 650))
    time.sleep(2)
    result = wx_func.recv_moment_gift(mode)
    my_mouse.left_click(hwnd, (230, 805))
    time.sleep(1)
    my_mouse.left_click(hwnd, (230, 805))
    time.sleep(1)
    return result


# 日常任务入口
def enter_task(hwnd, no, mode=None):
    my_mouse.left_click(hwnd, con.LOC_TASK)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_TASKLIST, mode=mode)
    if loc is None:
        logging.info('超时未进入任务列表界面，本次忽略处理')
        return EnterTaskResultEnum.fail
    page_size = 5
    item_height = 59
    first_btn = (345, 345)
    if no <= page_size:
        loc = (first_btn[0], first_btn[1] + (no - 1) * item_height)
    else:
        my_mouse.left_drag(hwnd, (290, 595), (290, 595 - (no - 5) * item_height))
        time.sleep(1)
        loc = (first_btn[0], first_btn[1] + 4 * item_height)
    # 检查是否为待处理
    match_loc = my_window.find_pic(hwnd, mode=mode, template_path=con.ID_TASK_TODO,
                                   loc_range=[(loc[0] - 30, loc[1] - 15), (loc[0] + 30, loc[1] + 15)])
    if match_loc is None:
        logging.info('该任务已完成，忽略处理')
        # 还原到原位置
        if no > page_size:
            my_mouse.left_drag(hwnd, (290, 335), (290, 335 + (no - 5) * item_height))
            time.sleep(0.5)
        rightdown_exit(hwnd)
        return EnterTaskResultEnum.finished

    my_mouse.left_click(hwnd, loc)
    time.sleep(1)
    return EnterTaskResultEnum.success


# 挖矿
def mine(hwnd, mode=None, concurrent=3):
    my_mouse.left_click(hwnd, con.LOC_UNION)
    time.sleep(1)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_UNION_VIEW, mode=mode)
    if loc is None:
        logging.info('超时未进入仙盟界面，本次忽略处理')
        return False
    time.sleep(1)
    my_mouse.left_click(hwnd, (430, 220))
    time.sleep(1)
    finish_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_MINE_FINISHED, mode=mode)
    if len(finish_list) > 0:
        logging.info('检测到存在已完成挖矿任务，进行领取')
        for item in finish_list:
            my_mouse.left_click(hwnd, item)
            time.sleep(1.5)
            rightdown_exit(hwnd)
    while True:
        # 领取矿石
        ore = my_window.find_pic(hwnd=hwnd, template_path=con.ID_MINE_ORE, mode=mode)
        if ore is not None:
            logging.info('检测到存在刷新出的矿石，进行领取')
            my_mouse.left_click(hwnd, ore)
            time.sleep(1)
        # 占领空矿
        empty_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_MINE_EMPTY, mode=mode)
        no_seat = False
        for item in empty_list:
            my_mouse.left_click(hwnd, item)
            time.sleep(1)
            seat = my_window.find_pic(hwnd=hwnd, template_path=con.ID_MINE_SEAT, mode=mode)
            if seat is not None:
                my_mouse.left_click(hwnd, seat)
                time.sleep(1)
                # 检测矿锄是否足够
                loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_MINE_LACK_OCCUPY, mode=mode)
                if loc is not None:
                    logging.info('检测到矿锄不足，无法占领')
                    no_seat = True
                else:
                    # 派遣
                    my_mouse.left_click(hwnd, (220, 670))
                    time.sleep(1.5)
            else:
                logging.info('未找到空位，本次忽略处理')
                no_seat = True
            # 返回
            rightdown_exit(hwnd)
        if no_seat:
            logging.info('存在未能占领成功的矿，本次忽略处理')
            break
        # 检测已占矿数
        none_list = my_window.find_pic_multi(hwnd=hwnd, template_path=con.ID_MINE_NONE, mode=mode)
        if len(none_list) <= (5 - concurrent):
            logging.info('已达到设置的同时占矿数，本次忽略处理')
            break
        if not my_util.in_progress('09:00', '21:00'):
            logging.info('未在可探寻时间范围内，不再执行刷新')
            break

        # 刷新
        my_mouse.left_click(hwnd, (320, 670))
        time.sleep(1)
        # 检测矿锄不足无法刷新的情况
        loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_MINE_LACK_REFRESH, mode=mode)
        if loc is not None:
            logging.info('检测到矿锄不足，无法刷新')
            break

    # 退出矿脉
    rightdown_exit(hwnd)
    # 退出仙盟
    union_exit(hwnd, mode)
    return True


# 掌门功法
def use_master_skill(hwnd, mode=my_window.MODE_BG):
    my_mouse.left_click(hwnd, (120, 165))
    time.sleep(1)
    my_mouse.left_click(hwnd, (285, 185))
    time.sleep(0.5)
    loc_list = my_window.find_pic_multi(hwnd, mode, template_path=con.ID_MASTER_SKILL_CANUSE)
    if loc_list is not None and len(loc_list) > 0:
        logging.info(f'检测到存在{len(loc_list)}个可使用掌门功法，开始使用...')
        star_loc = None
        for loc in loc_list:
            if loc[1] < 300:
                star_loc = loc
                continue
            elif loc[1] > 400:
                continue
            my_mouse.left_click(hwnd, loc)
            time.sleep(0.5)
        if star_loc is not None:
            my_mouse.left_click(hwnd, star_loc)
            time.sleep(8)
    rightdown_exit(hwnd)
    return True


# 检查章节任务
def check_chapter_reward(hwnd, mode=my_window.MODE_BG):
    while True:
        loc = my_window.find_click(hwnd=hwnd, mode=mode, template_path=con.ID_CHAPTER_REWARD)
        if loc is None:
            # todo 下个章节
            break
        else:
            logging.info('成功处理章节任务完成弹框')


# 盟战
def check_union_contend(hwnd, mode):
    weekday = my_util.weekday()
    if weekday < 6:
        return
    if not my_util.in_progress('20:00', '20:05'):
        return
    # todo 盟站


# 蛮荒礼包
def check_savagery_gift(hwnd, mode):
    if not my_util.in_progress('00:00', '00:05'):
        return


# 掌门突破
def check_master_breakthrough(hwnd, mode):
    loc = my_window.find_click(hwnd=hwnd, mode=mode, template_path=con.ID_MASTER_BREAKTHROUGH)
    if loc is None:
        return False
    enter_pointing(hwnd, mode)
    loc = my_window.wait_appear(hwnd=hwnd, template_path=con.ID_MASTER_VIEW, mode=mode)
    if loc is None:
        logging.info('进入掌门界面超时,本次忽略处理')
        return False
    # 进入修行
    my_mouse.left_click(hwnd, (45, 595))
    time.sleep(1)
    loc = my_window.find_any_pic(hwnd=hwnd, template_paths=con.BTN_MASTER_BREAKTHROUGH_TODO, mode=mode)
    if loc is not None:
        my_mouse.left_click(hwnd, (260, 595))
        time.sleep(1)
        my_mouse.left_click(hwnd, (220, 530))
        time.sleep(1)
        my_mouse.left_click(hwnd, (310, 525))
        time.sleep(1)
        loc = my_window.wait_any_appear(hwnd=hwnd, template_paths=con.ID_BREAKTHROUGH_RESULT, timeout=5,
                                        mode=mode)
        rightdown_exit(hwnd)
    my_mouse.left_click(hwnd, (20, 110))
    time.sleep(1)
    rightdown_exit(hwnd)
    return True


# 掌门功法升级
def check_master_skill(hwnd, mode):
    loc = my_window.find_click(hwnd=hwnd, mode=mode, template_path=con.ID_MASTER_SKILL_BREAKTHROUGH)
    if loc is None:
        return False
    enter_pointing(hwnd, mode)
    loc = my_window.wait_click(hwnd=hwnd, template_path=con.ID_MASTER_VIEW, mode=mode)
    if loc is None:
        logging.info('进入掌门界面超时,本次忽略处理')
        return False
    for i in range(0, 3):
        loc = my_window.find_click(hwnd=hwnd, template_path=con.ID_COMMA, mode=mode,
                                   loc_range=[(100, 230), (420, 650)])
        if loc is None:
            loc = my_window.find_click(hwnd=hwnd, template_path=con.ID_MASTER_SKILL_UNSEAL, mode=mode)
            if loc is not None:
                time.sleep(3)
                continue
            my_mouse.left_drag(hwnd, (365, 655), (365, 220))
            time.sleep(0.5)
            loc = my_window.find_click(hwnd=hwnd, template_path=con.ID_MASTER_SKILL_UNSEAL, mode=mode)
            time.sleep(3)
            continue

        for j in range(0, 2):
            loc = my_window.find_click(hwnd=hwnd, template_path=con.ID_COMMA, mode=mode,
                                       loc_range=[(100, 230), (420, 650)])
            if loc is None:
                my_mouse.left_drag(hwnd, (390, 580), (390, 350))
                time.sleep(0.5)
                continue
            my_mouse.left_click(hwnd, (270, 740))
            time.sleep(0.5)
            break
        break
    # 3次退出
    for i in range(0, 3):
        rightdown_exit(hwnd)
    return True


# 卡在游历界面检测
def check_travel(hwnd, mode):
    loc = my_window.find_pic(hwnd=hwnd, template_path=con.ID_TRAVEL_VIEW, mode=mode)
    if loc is not None:
        exit_travel(hwnd, mode)


# 兑换码
def redeem(hwnd, mode, caller=None, codes=None):
    if not is_main_view(hwnd, mode):
        logging.info('当前不处于主界面，忽略处理')
        return
    # 点击头像
    my_mouse.left_click(hwnd, (45, 110))
    time.sleep(1.5)
    # 点击设置
    my_mouse.left_click(hwnd, (80, 160))
    time.sleep(1)
    for code in codes.split(','):
        if caller.isStop:
            break
        my_mouse.left_click(hwnd, (230, 580))
        time.sleep(1)
        my_mouse.left_click(hwnd, (225, 470))
        time.sleep(1)
        my_window.send_msg(hwnd, code)
        # 确认
        my_mouse.left_click(hwnd, (160, 480))
        time.sleep(1)
        # 使用
        my_mouse.left_click(hwnd, (220, 550))
        time.sleep(1)
        # 两次点击返回设置
        for i in range(0, 2):
            my_mouse.left_click(hwnd, (220, 680))
            time.sleep(0.5)
    my_mouse.left_click(hwnd, (230, 805))
    time.sleep(1)
    my_mouse.left_click(hwnd, (230, 805))
    time.sleep(1)


# 检查分享链接（妖王/妖窟）有效性
def check_share(hwnd, loc, x_offset=0):
    x, y = loc
    start_x = x - 10 - x_offset
    start_y = y - 35
    loc_logo = my_window.find_any_pic(hwnd=hwnd, template_paths=con.ID_SHARE_LOGOS, mode=my_window.MODE_BG,
                                      loc_range=[(start_x, start_y), (start_x + 30, start_y + 30)])
    return loc_logo is not None


# 每执行完一轮任务进行此项检查，为加快处理速度仅第一步需要截屏
def check_round(hwnd, mode):
    # 断线
    check_offline(hwnd, mode)
    # 章节任务
    # check_chapter_reward(hwnd, mode)
    # 盟站
    # check_union_contend(hwnd, mode)
    # 蛮荒礼包
    # check_savagery_gift(hwnd, mode)
    # 卡在游历界面检测
    check_travel(hwnd, mode)
