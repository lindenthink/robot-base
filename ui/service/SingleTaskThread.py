import logging
import time
import traceback
from enum import Enum

from PyQt6.QtCore import QThread
from pynput.mouse import Button

from common import my_mouse
from common.my_cfg import ConfigKey, ConfigManager
from common.my_event import MouseListener
from gm import gm_func
from ui import MainWindow


class SingleKeyEnum(Enum):
    click = 'click'
    click_x = 'x'
    click_y = 'y'
    click_intv = 'intv'


class SingleTaskThread(QThread):
    single_tabs = [None, '妖窟材料', '斗技', '铸造分解', '观看广告', '兑换密令', '鼠标连点']
    mouse_listener = None

    def __init__(self, mainWnd, cfgMgr):
        super().__init__()
        self.isStop = False
        self.mainWnd: MainWindow = mainWnd
        self.cfgMgr: ConfigManager = cfgMgr
        if self.cfgMgr is not None:
            self.cfg = self.cfgMgr.single

    def init_6(self):
        key = SingleKeyEnum.click.value
        if key in self.cfg:
            click_cfg = self.cfg[SingleKeyEnum.click.value]
            x = click_cfg[SingleKeyEnum.click_x.value]
            y = click_cfg[SingleKeyEnum.click_y.value]
            intv = click_cfg[SingleKeyEnum.click_intv.value]
            self.mainWnd.spin_tools_click_x.setValue(x)
            self.mainWnd.spin_tools_click_y.setValue(y)
            self.mainWnd.spin_tools_click_intv.setValue(intv)

    def onEmitLoc(self, x, y):
        self.mainWnd.spin_tools_click_x.setValue(x)
        self.mainWnd.spin_tools_click_y.setValue(y)

    def onMouseMove(self, x, y):
        self.mainWnd.locSignal.emit(x, y)

    def onMouseClick(self, x, y, button, pressed):
        if button == Button.left and pressed:
            self.mouse_listener.stop()
            self.mainWnd.pushButton.setEnabled(True)

    def onRunLoc(self):
        self.mainWnd.pushButton.setEnabled(False)
        self.mainWnd.emitLeftTop()
        self.mouse_listener = MouseListener(on_move=self.onMouseMove, on_click=self.onMouseClick)
        self.mouse_listener.start()

    def bind_6(self):
        self.mainWnd.pushButton.clicked.connect(self.onRunLoc)
        # 信号只能在主窗口中定义
        self.mainWnd.locSignal.connect(self.onEmitLoc)

    def run_6(self):
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

    # 动态绑定
    def bind(self):
        for i in range(1, len(self.single_tabs)):
            if hasattr(self, f'bind_{i}'):
                func = getattr(self, f'bind_{i}')
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

    def currentMode(self):
        return self.cfgMgr.getArg(ConfigKey.args_mode)
