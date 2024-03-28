import logging
import time
import traceback
from enum import Enum

from PyQt6.QtCore import QThread
from PyQt6.QtGui import QPixmap
from pynput.mouse import Button

import dirs
from common import my_mouse, my_service
from common.my_cfg import ConfigKey, ConfigManager
from common.my_event import MouseListener
from gm import gm_func
from ui import MainWindow


class SingleKeyEnum(Enum):
    click = 'click'
    click_x = 'x'
    click_y = 'y'
    click_intv = 'intv'

    ad = 'ad'
    ad_useSand = 'useSand'

    foundry = 'foundry'
    foundry_level = 'level'
    foundry_qlty = 'qlty'
    foundry_round = 'round'

    contend = 'contend'
    contend_count = 'count'
    contend_fight3rd = 'fight3rd'
    contend_3peed = 'tripleSpeed'
    contend_rightexit = 'rightExit'

    boss = 'boss'
    boss_count = 'count'
    boss_qlty = 'qlty'
    boss_type = 'type'
    boss_farm = 'farm'
    boss_farm_intv = 'farmInterval'
    boss_farm_cost = 'useMoney'


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

    def init_1(self):
        key = SingleKeyEnum.boss.value
        if key in self.cfg:
            sub_cfg = self.cfg[key]
            self.mainWnd.spin_boss_count.setValue(sub_cfg[SingleKeyEnum.boss_count.value])
            self.mainWnd.check_boss_qlty_hard.setChecked('难' in sub_cfg[SingleKeyEnum.boss_qlty.value])
            self.mainWnd.check_boss_qlty_mid.setChecked('中' in sub_cfg[SingleKeyEnum.boss_qlty.value])
            self.mainWnd.check_boss_type_bird.setChecked('鸟' in sub_cfg[SingleKeyEnum.boss_type.value])
            self.mainWnd.check_boss_type_phoenix.setChecked('凤' in sub_cfg[SingleKeyEnum.boss_type.value])
            self.mainWnd.check_boss_type_snake.setChecked('蛇' in sub_cfg[SingleKeyEnum.boss_type.value])
            self.mainWnd.check_boss_type_crab.setChecked('蟹' in sub_cfg[SingleKeyEnum.boss_type.value])
            self.mainWnd.check_boss_type_fish.setChecked('鱼' in sub_cfg[SingleKeyEnum.boss_type.value])
            self.mainWnd.check_boss_farm.setChecked(sub_cfg[SingleKeyEnum.boss_farm.value])
            self.mainWnd.spin_boss_farm_intv.setValue(sub_cfg[SingleKeyEnum.boss_farm_intv.value])
            if SingleKeyEnum.boss_farm_cost.value in sub_cfg:
                self.mainWnd.check_boss_use_money.setChecked(sub_cfg[SingleKeyEnum.boss_farm_cost.value])

    def run_1(self):
        sub_cfg = dict()
        count = self.mainWnd.spin_boss_count.value()
        qualities = list()
        if self.mainWnd.check_boss_qlty_hard.isChecked():
            qualities.append('难')
        if self.mainWnd.check_boss_qlty_mid.isChecked():
            qualities.append('中')
        types = list()
        if self.mainWnd.check_boss_type_fish.isChecked():
            types.append('鸟')
        if self.mainWnd.check_boss_type_phoenix.isChecked():
            types.append('凤')
        if self.mainWnd.check_boss_type_snake.isChecked():
            types.append('蛇')
        if self.mainWnd.check_boss_type_crab.isChecked():
            types.append('蟹')
        if self.mainWnd.check_boss_type_fish.isChecked():
            types.append('鱼')
        farm = self.mainWnd.check_boss_farm.isChecked()
        farm_interval = self.mainWnd.spin_boss_farm_intv.value()
        use_money = self.mainWnd.check_boss_use_money.isChecked()
        sub_cfg[SingleKeyEnum.boss_count.value] = count
        sub_cfg[SingleKeyEnum.boss_qlty.value] = qualities
        sub_cfg[SingleKeyEnum.boss_type.value] = types
        sub_cfg[SingleKeyEnum.boss_farm.value] = farm
        sub_cfg[SingleKeyEnum.boss_farm_intv.value] = farm_interval
        sub_cfg[SingleKeyEnum.boss_farm_cost.value] = use_money
        self.cfg[SingleKeyEnum.boss.value] = sub_cfg
        self.cfgMgr.saveTasks()
        gm_func.single_boss(gm_func.get_hwnd(), mode=self.currentMode(), count=count, qualities=qualities, types=types,
                            farm=farm, farm_interval=farm_interval, caller=self, use_money=use_money)

    def init_2(self):
        key = SingleKeyEnum.contend.value
        if key in self.cfg:
            sub_cfg = self.cfg[key]
            self.mainWnd.spin_ctd_count.setValue(sub_cfg[SingleKeyEnum.contend_count.value])
            self.mainWnd.check_ctd_fight3rd.setChecked(sub_cfg[SingleKeyEnum.contend_fight3rd.value])
            self.mainWnd.check_ctd_3speed.setChecked(sub_cfg[SingleKeyEnum.contend_3peed.value])
            self.mainWnd.check_ctd_rightexit.setChecked(sub_cfg[SingleKeyEnum.contend_rightexit.value])

    def run_2(self):
        sub_cfg = dict()
        count = self.mainWnd.spin_ctd_count.value()
        is_triple = self.mainWnd.check_ctd_fight3rd.isChecked()
        right_exit = self.mainWnd.check_ctd_rightexit.isChecked()
        fight_3rd = self.mainWnd.check_ctd_3speed.isChecked()
        sub_cfg[SingleKeyEnum.contend_count.value] = count
        sub_cfg[SingleKeyEnum.contend_3peed.value] = is_triple
        sub_cfg[SingleKeyEnum.contend_rightexit.value] = right_exit
        sub_cfg[SingleKeyEnum.contend_fight3rd.value] = fight_3rd
        self.cfg[SingleKeyEnum.contend.value] = sub_cfg
        self.cfgMgr.saveTasks()
        gm_func.contend(gm_func.get_hwnd(), mode=self.currentMode(), count=count, is_triple=is_triple,
                        right_exit=right_exit, fight_3rd=fight_3rd, caller=self)

    def init_3(self):
        key = SingleKeyEnum.foundry.value
        if key in self.cfg:
            sub_cfg = self.cfg[key]
            self.mainWnd.combo_fdry_level.setCurrentIndex(sub_cfg[SingleKeyEnum.foundry_level.value])
            self.mainWnd.combo_fdry_qlty.setCurrentIndex(sub_cfg[SingleKeyEnum.foundry_qlty.value])
            self.mainWnd.spin_fdry_round.setValue(sub_cfg[SingleKeyEnum.foundry_round.value])

    def run_3(self):
        sub_cfg = dict()
        level = self.mainWnd.combo_fdry_level.currentIndex()
        dec_qlty = self.mainWnd.combo_fdry_qlty.currentIndex()
        dec_round = self.mainWnd.spin_fdry_round.value()
        sub_cfg[SingleKeyEnum.foundry_level.value] = level
        sub_cfg[SingleKeyEnum.foundry_qlty.value] = dec_qlty
        sub_cfg[SingleKeyEnum.foundry_round.value] = dec_round
        self.cfg[SingleKeyEnum.foundry.value] = sub_cfg
        self.cfgMgr.saveTasks()
        gm_func.foundry(gm_func.get_hwnd(), mode=self.currentMode(), level=level + 1, caller=self,
                        dec_qlty=dec_qlty + 2, dec_round=dec_round)

    def init_4(self):
        pic_exchange = QPixmap(dirs.join_data('ad.jpg'))
        self.mainWnd.lab_ad.setPixmap(pic_exchange)
        key = SingleKeyEnum.ad.value
        if key in self.cfg:
            sub_cfg = self.cfg[key]
            self.mainWnd.check_ad_timesand.setChecked(sub_cfg[SingleKeyEnum.ad_useSand.value])

    def run_4(self):
        sub_cfg = dict()
        use_sand = self.mainWnd.check_ad_timesand.isChecked()
        sub_cfg[SingleKeyEnum.ad_useSand.value] = use_sand
        self.cfg[SingleKeyEnum.ad.value] = sub_cfg
        self.cfgMgr.saveTasks()
        gm_func.watch_ad(gm_func.get_hwnd(), mode=self.currentMode(), use_timesand=use_sand, caller=self)

    def run_5(self):
        is_weekly = self.mainWnd.radio_week.isChecked()
        data_type = 'WEEKLY' if is_weekly else 'COMMON'
        login_info = self.mainWnd.loginInfo
        res = my_service.checkRedeem(login_info.username, login_info.password, game=login_info.gmCode,
                                     enc_key=login_info.encKey, data_type=data_type)
        if res['code'] == -1:
            logging.info(f'操作失败：{res["message"]}')
            return
        codes = None if 'codes' not in res['data'] else res['data']['codes']
        if codes is None:
            logging.info('当前不存在有效兑换码，忽略处理')
            return
        gm_func.redeem(gm_func.get_hwnd(), self.currentMode(), caller=self, codes=codes)

    def init_6(self):
        key = SingleKeyEnum.click.value
        if key in self.cfg:
            sub_cfg = self.cfg[SingleKeyEnum.click.value]
            x = sub_cfg[SingleKeyEnum.click_x.value]
            y = sub_cfg[SingleKeyEnum.click_y.value]
            intv = sub_cfg[SingleKeyEnum.click_intv.value]
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

        sub_cfg = dict()
        sub_cfg[SingleKeyEnum.click_x.value] = x
        sub_cfg[SingleKeyEnum.click_y.value] = y
        sub_cfg[SingleKeyEnum.click_intv.value] = intv
        self.cfg[SingleKeyEnum.click.value] = sub_cfg
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
