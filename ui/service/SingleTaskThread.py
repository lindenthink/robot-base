import logging
import time
import traceback
from enum import Enum

from PyQt6.QtCore import QThread

from common import my_mouse
from common.my_cfg import ConfigKey, ConfigManager
from gm import gm_func
from ui import MainWindow


class SingleKeyEnum(Enum):
    click = 'click'
    click_x = 'x'
    click_y = 'y'
    click_intv = 'intv'


class SingleTaskThread(QThread):
    single_tabs = [None, '鼠标连击']

    def __init__(self, mainWnd, cfgMgr):
        super().__init__()
        self.isStop = False
        self.mainWnd: MainWindow = mainWnd
        self.cfgMgr: ConfigManager = cfgMgr
        self.cfg = self.cfgMgr.single

    def init_1(self):
        key = SingleKeyEnum.click.value
        if key in self.cfg:
            click_cfg = self.cfg[SingleKeyEnum.click.value]
            x = click_cfg[SingleKeyEnum.click_x.value]
            y = click_cfg[SingleKeyEnum.click_y.value]
            intv = click_cfg[SingleKeyEnum.click_intv.value]
            self.mainWnd.spin_tools_click_x.setValue(x)
            self.mainWnd.spin_tools_click_y.setValue(y)
            self.mainWnd.spin_tools_click_intv.setValue(intv)

    def run_1(self):
        x = self.mainWnd.spin_tools_click_x.value()
        y = self.mainWnd.spin_tools_click_y.value()
        intv = self.mainWnd.spin_tools_click_intv.value()

        click_cfg = dict()
        click_cfg[SingleKeyEnum.click_x.value] = x
        click_cfg[SingleKeyEnum.click_y.value] = y
        click_cfg[SingleKeyEnum.click_intv.value] = intv
        self.cfg[SingleKeyEnum.click.value] = click_cfg
        self.cfgMgr.saveTasks()
        while True:
            if self.isStop:
                break
            my_mouse.left_click(gm_func.get_hwnd(), (x, y))
            time.sleep(intv / 1000)

    # 动态初始化
    def init(self):
        for i in range(1, len(self.single_tabs)):
            if hasattr(self, f'init_{i}'):
                func = getattr(self, f'init_{i}')
                func()

    # 动态执行
    def run(self):
        self.isStop = False
        active_index = self.mainWnd.wid_tab.currentIndex()
        active_tab = self.single_tabs[active_index]
        logging.info(f'开始执行【{active_tab}】...')
        if gm_func.get_hwnd() <= 0:
            logging.info(msg='目标窗口不存在，忽略处理')
            return
        try:
            func = getattr(self, f'run_{active_index}')
            func()
            logging.info(f'【{active_tab}】执行完成')
        except Exception as e:
            logging.info(f'【{active_tab}】执行失败：{e}')
            print(traceback.format_exc())

    def stop(self):
        self.isStop = True

    def current_mode(self):
        return self.cfgMgr.getArg(ConfigKey.args_mode)
