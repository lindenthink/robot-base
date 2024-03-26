import logging
import traceback

from PyQt6.QtCore import QThread, QWaitCondition, QMutex

from common import my_window
from common.my_cfg import ConfigKey
from gm import gm_func
from ui.service.IconTypeEnum import IconTypeEnum


class MainloopThread(QThread):
    def __init__(self, mainWnd, cfgMgr):
        super().__init__()
        self.cfgMgr = cfgMgr
        self.isStop = False
        self.mainWnd = mainWnd
        self.cond = QWaitCondition()
        self.mutex = QMutex()

    def run(self):
        self.mutex.lock()
        mode = self.cfgMgr.getArg(ConfigKey.args_mode)
        mode_name = '前台模式' if mode == my_window.MODE_FG else '后台模式'
        logging.info(f'开始以{mode_name}执行')
        check_pass = gm_func.readiness_check(gm_func.get_hwnd(), mode=mode)
        if not check_pass:
            self.mainWnd.onStop()
            return
        while True:
            try:
                gm_func.check_round(gm_func.get_hwnd(), mode=mode)
                if self.cfgMgr.checkReset():
                    self.mainWnd.emitReset()
                    logging.warning('检测到当日首次执行，已自动重置所有任务')
                for task in self.cfgMgr.tasks:
                    if self.isStop:
                        break
                    if task.isDone():
                        continue
                    if not gm_func.is_main_view(gm_func.get_hwnd(), mode=mode):
                        break
                    gm_func.check_notice(gm_func.get_hwnd(), mode=mode)
                    self.mainWnd.emitIcon(IconTypeEnum.running, task.name)
                    if task.run(self.cfgMgr.args):
                        self.cfgMgr.saveTasks()
                    if task.isDone():
                        self.mainWnd.emitIcon(IconTypeEnum.finished, task.name)
                    else:
                        self.mainWnd.emitIcon(IconTypeEnum.none, task.name)
            except Exception as e:
                logging.error(e)
                print(traceback.format_exc())
            if self.isStop:
                break
            self.sleep(1)
        self.mutex.unlock()

    def stop(self):
        logging.info('停止执行')
        self.isStop = True
