from os import path

import dirs

TITLE = '微信'
# 微信主窗口类名
WND_CLASS = 'WeChatMainWndForPC'
# 聊天窗口类
CHAT_CLASS = 'ChatWnd'
# 微信小游戏、游戏圈附属窗口
SUBWND_CLASS = 'Chrome_WidgetWin_0'
# 确认框窗口类
CONFIRM_CLASS = 'ConfirmDialog'

# 图片根路径
PATH_IMG = path.join(dirs.templates_path(), 'wx')


def join(name):
    return path.join(PATH_IMG, f'{name}.jpg')


# 广告完成标识
ID_AD_FINISH = join('id_ad_finish')
# 广告弹窗关关闭
BTN_AD_POP_CLOSE = join('btn_ad_pop_close')

# 微信游戏圈标识
ID_MOMENT = join('id_moment')
# 微信游戏圈一键领取标识
BTN_MOMENT_RECV = join('btn_moment_recv')
# 道天录游戏圈领取成功
ID_MOMENT_SUCCESS = join('id_moment_success')

# 指定待打开小程序图标
ID_MINI_GM_LIST = [join('id_mini_gm'), join('id_mini_gm2')]

# 关闭广告
LOC_AD_CLOSE = (410, 70)
# 小程序入口
LOC_MINI = (25, 525)
