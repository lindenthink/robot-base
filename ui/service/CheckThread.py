from datetime import datetime

from PyQt6.QtCore import QThread

from common import my_service, my_util
from ui.service.StatusTypeEnum import StatusTypeEnum
from ui.service.LoginInfo import LoginInfo


class CheckThread(QThread):
    interval = 1

    def __init__(self, mainWnd):
        super().__init__()
        self.mainWnd = mainWnd
        self.loginInfo: LoginInfo = mainWnd.loginInfo

    def run(self):
        count = 0
        while True:
            if self.loginInfo.username is not None:
                self.checkAccount()
                count += 1
                if count == 60:
                    self.checkVersion()
                    count = 0
                    self.sleep(60)
            self.sleep(self.interval)

    def checkAccount(self):
        expireTime = my_util.parseDateTime(self.loginInfo.expireTime)
        nowTime = datetime.now()
        if expireTime <= nowTime:
            for remain in range(59, -1, -1):
                self.mainWnd.emitStatus(StatusTypeEnum.error, f'您的账号已过期，{remain}秒内未充值将自动退出 o(╥﹏╥)o')
                self.sleep(1)
                # 再次检查一遍是否完成充值
                expireTime = my_util.parseDateTime(self.loginInfo.expireTime)
                if expireTime > nowTime:
                    return
            self.mainWnd.emitLogout()
            return
        # 单任务执行时需要占用状态栏输出信息
        if self.mainWnd.isSingleRun:
            return
        status_type = StatusTypeEnum.info
        interval = expireTime - nowTime
        interval_days = interval.days

        hint = '感谢支持 ✿✿ヽ(°▽°)ノ✿'
        if interval_days < 4:
            status_type = StatusTypeEnum.warn
            hint = '为避免正常使用，请关注并及时充值呦 ლ(╹◡╹ლ)'
        if interval_days < 1:
            status_type = StatusTypeEnum.error
            hint = '到期将自动退出登录，得尽快充值啦 ヾ(◍°∇°◍)ﾉﾞ'
        interval_seconds = interval.seconds  # 除去天数的总秒数
        days = interval_days
        hours = interval_seconds // (60 * 60)
        minutes = (interval_seconds - hours * 60 * 60) // 60
        seconds = interval_seconds - hours * 60 * 60 - minutes * 60
        self.mainWnd.emitStatus(status_type, f'您的账号剩余时间为{days}天{hours}时{minutes}分{seconds}秒，{hint}')

    def checkVersion(self):
        inuse_version = self.loginInfo.gmVer
        res = my_service.checkVersion(self.loginInfo.username, self.loginInfo.password,
                                      inuse_version, game=self.loginInfo.gmCode,
                                      enc_key=self.loginInfo.encKey)
        if res['code'] == -1:
            self.mainWnd.emitStatus(StatusTypeEnum.error, f'检测到账号状态异常将自动退出，请重新登陆 Σ(⊙▽⊙\"')
            self.mainWnd.emitLogout()
        elif res['code'] == -2:
            self.mainWnd.emitStatus(StatusTypeEnum.error, f'检测版本失败：网络连接异常 ╰(*°▽°*)╯')
        else:
            if res['data']['match']:
                self.mainWnd.emitStatus(StatusTypeEnum.success, f'当前应用版本号为「{inuse_version}」，已是最新版本 ✿✿ヽ(°▽°)ノ✿')
            else:
                self.mainWnd.emitStatus(StatusTypeEnum.warn,
                                        f'当前版本「{inuse_version}」，检测到新版本「{res["data"]["newVersion"]}」，可通过「系统-检查版本」进行下载升级 (〃\'▽\'〃)')
