import _thread
import logging
import sys
import webbrowser

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor, QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMenu, QListWidgetItem, QTreeWidgetItem, QMessageBox, QDialog, QButtonGroup, \
    QInputDialog, QLineEdit

import dirs
from common import my_window, my_cfg, my_service
from common.my_cfg import ConfigKey
from gm import gm_func
from .LoginDialog import LoginDialog
from .MainWindow_Ui import Ui_MainWindow
from .TaskOptionDialog import TaskOptionDialog
from ui.service import SingleTaskThread, LoginInfo, MainloopThread, CheckThread, StatusTypeEnum, IconTypeEnum


class MainWindow(QMainWindow, Ui_MainWindow):
    logSignal = pyqtSignal(str)
    logoutSignal = pyqtSignal()
    statusSignal = pyqtSignal(StatusTypeEnum, str)
    iconSignal = pyqtSignal(IconTypeEnum, str)
    resetSignal = pyqtSignal()
    loginSignal = pyqtSignal()

    isRun = False
    isSingleRun = False

    loginInfo = LoginInfo()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
        self.initData()
        self.bindEvent()

        checkThread = CheckThread(self)
        checkThread.start()
        self.show()
        _thread.start_new_thread(self.loginSignal.emit, ())

    @staticmethod
    def onRightTop():
        target_hwnd = gm_func.get_hwnd()
        if target_hwnd == 0:
            logging.info('未能获取到游戏窗口')
            return
        my_window.move_rt(target_hwnd)

    @staticmethod
    def onContact():
        my_window.show_img(dirs.join_data('contact.jpg'))

    @staticmethod
    def onLeftTop():
        target_hwnd = gm_func.get_hwnd()
        if target_hwnd == 0:
            logging.info('未能获取到游戏窗口')
            return
        my_window.move_lt(target_hwnd)

    def initUi(self):
        # 固定窗口大小
        self.setFixedSize(self.width(), self.height())

        pic_exchange = QPixmap(dirs.join_data('exchange.jpg'))
        self.lab_exchange.setPixmap(pic_exchange)
        self.grp_mode = QButtonGroup()
        self.grp_mode.addButton(self.radio_bg)
        self.grp_mode.addButton(self.radio_fg)
        self.grp_loc = QButtonGroup()
        self.grp_loc.addButton(self.radio_righttop)
        self.grp_loc.addButton(self.radio_lefttop)

    def initData(self):
        self.meta = my_cfg.loadMeta()

        self.loginInfo.gmName = self.meta['name']
        self.loginInfo.gmCode = self.meta['code']
        self.loginInfo.gmVer = self.meta['ver']
        # 设置标题和Logo
        self.setWindowTitle(f'菩提思 | {self.loginInfo.gmName}')
        icon = QIcon()
        icon.addPixmap(QPixmap(dirs.join_data('logo.jpg')), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)

        # 初始化任务树视图
        self.initTaskTree()

    def initTaskList(self):
        for task in self.cfgMgr.tasks:
            item = QListWidgetItem(self.list_todo)
            if task.isDone():
                self.changeTaskIcon(iconType=IconTypeEnum.finished, item=item)
            item.setText(task.name)
            self.list_todo.addItem(item)

    def initTaskTree(self):
        meta_tasks = self.meta['tasks']
        p = 0
        c = 0
        group = None
        disable_icon = QIcon()
        disable_icon.addPixmap(QPixmap(IconTypeEnum.disable.value), QIcon.Mode.Normal, QIcon.State.Off)
        for meta_task in meta_tasks:
            if 'group' not in meta_task:
                item_0 = QTreeWidgetItem(self.tree_tasks)
                # 处理禁用
                if not meta_task['enable']:
                    item_0.setIcon(0, disable_icon)
                    item_0.setFlags(
                        Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsUserCheckable
                        | Qt.ItemFlag.ItemIsEnabled)
                self.tree_tasks.topLevelItem(p).setText(0, meta_task['name'])
                p += 1
                c = 0
                group = None
                continue
            if group != meta_task['group']:
                c = 0
            if c == 0:
                # 添加新分组
                group = meta_task['group']
                item_0 = QTreeWidgetItem(self.tree_tasks)
                # 不可选中分组
                item_0.setFlags(
                    Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsUserCheckable
                    | Qt.ItemFlag.ItemIsEnabled)
                self.tree_tasks.topLevelItem(p).setText(0, group)
                p += 1
            item_1 = QTreeWidgetItem(item_0)
            # 处理禁用
            if not meta_task['enable']:
                item_1.setIcon(0, disable_icon)
                item_1.setFlags(
                    Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsUserCheckable
                    | Qt.ItemFlag.ItemIsEnabled)
            self.tree_tasks.topLevelItem(p - 1).child(c).setText(0, meta_task['name'])
            c += 1

    def bindEvent(self):
        self.logSignal.connect(self.appendLog)
        self.statusSignal.connect(self.onStatusChange)
        self.iconSignal.connect(self.onIconChange)
        self.logoutSignal.connect(self.onLogout)
        self.resetSignal.connect(self.resetAllIcon)
        self.loginSignal.connect(self.onLogin)

        self.bindMenuEvent()
        self.bindTabTaskEvent()
        self.btn_run.clicked.connect(self.onRun)
        self.btn_stop.clicked.connect(self.onStop)

    def bindMenuEvent(self):
        self.menu_login.triggered.connect(self.onLogin)
        self.menu_reg.triggered.connect(self.onReg)
        self.menu_logout.triggered.connect(self.onLogout)
        self.menu_modifypwd.triggered.connect(self.onModifyPwd)
        self.menu_recharge.triggered.connect(self.onRecharge)
        self.menu_versioncheck.triggered.connect(self.onCheckVersionActive)
        self.menu_help.triggered.connect(self.onHelp)
        self.menu_contact.triggered.connect(self.onContact)
        self.menu_exit.triggered.connect(sys.exit)

    def bindTabTaskEvent(self):
        self.text_log.customContextMenuRequested.connect(self.onLogMenu)
        self.tree_tasks.customContextMenuRequested.connect(self.onMetaMenu)
        self.list_todo.customContextMenuRequested.connect(self.onTaskMenu)

        self.btn_reset.clicked.connect(self.onResetAllTasks)
        self.btn_remove.clicked.connect(self.onRemoveAllTasks)
        self.btn_recommend.clicked.connect(self.onRecommend)

        self.radio_fg.clicked.connect(self.onFg)
        self.radio_bg.clicked.connect(self.onBg)
        self.radio_lefttop.clicked.connect(self.onLeftTop)
        self.radio_righttop.clicked.connect(self.onRightTop)
        self.check_top.clicked.connect(self.onFix)

        self.tree_tasks.itemDoubleClicked.connect(self.onDbAddTask)
        self.list_todo.itemDoubleClicked.connect(self.onDbRemoveTask)

    def onLogin(self):
        login_ui = LoginDialog(self.loginInfo)
        if login_ui.exec() == QDialog.DialogCode.Accepted:
            self.afterLogin()

    def onReg(self):
        login_ui = LoginDialog(self.loginInfo)
        login_ui.radio_reg.click()
        if login_ui.exec() == QDialog.DialogCode.Accepted:
            self.afterLogin()

    def afterLogin(self):
        self.cfgMgr = my_cfg.ConfigManager(game=self.loginInfo.gmCode, user=self.loginInfo.username)
        # 参数初始化
        if self.cfgMgr.getArg(ConfigKey.args_mode) == my_window.MODE_FG:
            self.radio_fg.setChecked(True)
        else:
            self.radio_bg.setChecked(True)
        self.menu_login.setEnabled(False)
        self.menu_reg.setEnabled(False)
        self.menu_recharge.setEnabled(True)
        self.menu_modifypwd.setEnabled(True)
        self.menu_logout.setEnabled(True)
        self.menu_versioncheck.setEnabled(True)
        self.wid_tab.setEnabled(True)
        self.group_run.setEnabled(True)

        # 加载待执行任务列表
        self.initTaskList()

        # 初始化其他任务视图
        SingleTaskThread(self, self.cfgMgr).init()

        logging.info(f'欢迎{self.loginInfo.username}，您的账号于{self.loginInfo.expireTime}到期，游戏愉快 (*^▽^*)')
        # 触发版本更新提示
        self.onCheckVersion(active=False)

    def onHelp(self):
        webbrowser.open(self.meta['help'], new=0, autoraise=True)

    def onLogout(self):
        if self.isRun:
            self.onStop()
        self.group_run.setEnabled(False)
        self.list_todo.clear()
        self.menu_login.setEnabled(True)
        self.menu_reg.setEnabled(True)
        self.menu_recharge.setEnabled(False)
        self.menu_modifypwd.setEnabled(False)
        self.menu_logout.setEnabled(False)
        self.menu_versioncheck.setEnabled(False)
        self.wid_tab.setEnabled(False)
        self.loginInfo.username = None

    def onModifyPwd(self):
        text, ok = QInputDialog.getText(self, '菩提思 | 修改密码', "请输入新密码：", QLineEdit.EchoMode.Password)
        if ok:
            if self.username is None:
                QMessageBox.critical(self, '操作失败', '修改密码失败，需要登陆后方可进行此操作。')
                return
            new_password = str(text)
            if new_password is None or len(new_password) < 6:
                QMessageBox.critical(self, '操作失败', '修改密码失败，密码不能为空并且长度不少于6位。')
                return
            res = my_service.modifyPwd(self.username, self.password, new_password, game=self.code, enc_key=self.encKey)
            if res['code'] == -1:
                QMessageBox.critical(self, '操作失败', f'{res["message"]}')
                return
            else:
                QMessageBox.information(self, '操作提示', '修改成功，请保存好新密码')
                self.password = new_password
                return

    def onRecharge(self):
        text, ok = QInputDialog.getText(self, '菩提思 | 充值', "请输入充值码:")
        if ok:
            if self.username is None:
                QMessageBox.critical(self, '操作失败', '修改密码失败，需要登陆后方可进行此操作。')
                return
            cdk = str(text)
            if cdk is None or len(cdk) < 16:
                QMessageBox.critical(self, '操作失败', '充值码格式错误，请确认并重新操作。')
                return
            res = my_service.activate(self.username, code=cdk, game=self.code, enc_key=self.encKey)
            if res['code'] == -1:
                QMessageBox.critical(self, '操作失败', f'{res["message"]}')
            else:
                self.expireTime = res['data']['expireTime']
                QMessageBox.information(self, '操作提示', '充值成功，')

    def onCheckVersionActive(self):
        self.onCheckVersion(active=True)

    def onCheckVersion(self, active=True):
        inuse_version = self.meta['ver']
        res = my_service.checkVersion(self.loginInfo.username, self.loginInfo.password,
                                      inuse_version, game=self.meta['code'],
                                      enc_key=self.loginInfo.encKey)
        if res['code'] < 0:
            if active:
                QMessageBox.critical(self, '操作失败', f'{res["message"]}')
        else:
            if res['data']['match']:
                if active:
                    QMessageBox.information(self, '操作提示', '当前已是最新版本，无需更新！')
            else:
                button = QMessageBox.question(self, '操作确认', f'发现新版本「{res["data"]["newVersion"]}」，'
                                                            f'是否前往下载？ \r\n更新内容：\r\n{res["data"]["content"]}')
                if button == QMessageBox.StandardButton.Yes:
                    webbrowser.open(res['data']['downloadUrl'], new=0, autoraise=True)

    def onMetaMenu(self):
        items = self.tree_tasks.selectedItems()
        if items is None or len(items) == 0:
            return
        menu = QMenu(self.tree_tasks)
        act_add = QAction('添加', menu)
        act_add.triggered.connect(self.onAddTask)
        menu.addAction(act_add)
        menu.exec(QCursor.pos())

    def onTaskMenu(self):
        items = self.list_todo.selectedItems()
        if items is None or len(items) == 0:
            return
        menu = QMenu(self.list_todo)
        act_edit = QAction('选项', menu)
        act_edit.triggered.connect(self.onEditTask)
        act_remove = QAction('移除', menu)
        act_remove.triggered.connect(self.onRemoveTask)
        act_reset = QAction('重置', menu)
        act_reset.triggered.connect(self.onResetTask)
        act_success = QAction('完成', menu)
        act_success.triggered.connect(self.onSucceedTask)

        menu.addAction(act_edit)
        menu.addAction(act_remove)
        menu.addAction(act_reset)
        menu.addAction(act_success)
        menu.exec(QCursor.pos())

    def onLogMenu(self):
        menu = QMenu(self.text_log)
        act_clean = QAction('清空', menu)
        act_clean.triggered.connect(self.onCleanLog)
        menu.addAction(act_clean)
        menu.exec(QCursor.pos())

    def onCleanLog(self):
        self.text_log.clear()

    def onRun(self):
        self.isRun = True
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.radio_bg.setEnabled(False)
        self.radio_fg.setEnabled(False)
        self.wid_tab.setEnabled(False)
        active_index = self.wid_tab.currentIndex()
        if active_index == 0:
            self.saveTaskList()
            self.mainThread = MainloopThread(self, self.cfgMgr)
            run_thread = self.mainThread
        else:
            self.singleThread = SingleTaskThread(self, self.cfgMgr)
            self.singleThread.finished.connect(self.onStop)
            run_thread = self.singleThread
        run_thread.start()

    def onStop(self):
        if not self.isRun:
            return
        self.isRun = False
        active_index = self.wid_tab.currentIndex()
        if active_index == 0:
            self.mainThread.stop()
        else:
            self.singleThread.stop()
        self.btn_stop.setEnabled(False)
        self.btn_run.setEnabled(True)
        self.radio_bg.setEnabled(True)
        self.radio_fg.setEnabled(True)
        self.wid_tab.setEnabled(True)

    def onFg(self):
        self.cfgMgr.updArg(ConfigKey.args_mode, my_window.MODE_FG)

    def onBg(self):
        self.cfgMgr.updArg(ConfigKey.args_mode, my_window.MODE_BG)

    def saveTaskList(self):
        tmp_tasks = []
        for i in range(self.list_todo.count()):
            item = self.list_todo.item(i)
            for task in self.cfgMgr.tasks:
                if item.text() == task.name:
                    tmp_tasks.append(task)
                    break
        self.cfgMgr.tasks = tmp_tasks
        self.cfgMgr.saveTasks()

    def emitLog(self, text):
        self.logSignal.emit(text)

    def emitStatus(self, tp, text):
        self.statusSignal.emit(tp, text)

    def emitIcon(self, tp, name):
        self.iconSignal.emit(tp, name)

    def emitLogout(self):
        self.logoutSignal.emit()

    def emitReset(self):
        self.resetSignal.emit()

    def appendLog(self, text):
        self.text_log.appendPlainText(text)
        scroll_bar = self.text_log.verticalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def onDbAddTask(self, it, col):
        items = self.tree_tasks.selectedItems()
        if items is None or len(items) == 0:
            return
        task_name = items[0].text(0)
        if self.isTaskExists(task_name):
            QMessageBox.critical(self, '提示', '任务已存在，不能重复添加！')
            return
        item = QListWidgetItem(self.list_todo)
        item.setText(task_name)

        for task_meta in self.meta['tasks']:
            if task_meta['name'] == task_name:
                self.cfgMgr.addTask(task_meta)
                break
        self.list_todo.addItem(item)

    def isTaskExists(self, name):
        items = self.list_todo.findItems(name, Qt.MatchFlag.MatchFixedString)
        return len(items) > 0

    def changeTaskIcon(self, name=None, iconType=None, item=None, select=False):
        if item is None:
            item = self.list_todo.findItems(name, Qt.MatchFlag.MatchFixedString)[0]
        if select:
            self.list_todo.scrollToItem(item)
            item.setSelected(True)
        icon = QIcon()
        icon.addPixmap(QPixmap(iconType.value), QIcon.Mode.Normal, QIcon.State.Off)
        item.setIcon(icon)

    def onAddTask(self):
        self.onDbAddTask(None, None)

    def onDbRemoveTask(self, it):
        for i in range(self.list_todo.count()):
            if self.list_todo.item(i).isSelected():
                # 选出可使该item与QListWidget断开联系,然后才能将其删除
                item = self.list_todo.takeItem(i)
                self.cfgMgr.removeTask(item.text())
                self.list_todo.removeItemWidget(item)
                break

    def onRemoveTask(self):
        self.onDbRemoveTask(None)

    def onResetTask(self):
        item = self.list_todo.selectedItems()[0]
        task_name = item.text()
        self.changeTaskIcon(iconType=IconTypeEnum.none, item=item)
        self.cfgMgr.resetTaskByName(task_name)
        QMessageBox.information(self, '操作提示', '重置成功，将触发重新执行！')

    def onSucceedTask(self):
        item = self.list_todo.selectedItems()[0]
        task_name = item.text()
        self.changeTaskIcon(iconType=IconTypeEnum.finished, item=item)
        self.cfgMgr.succeedTask(task_name)
        QMessageBox.information(self, '操作提示', '已设置任务为完成状态，当日不再触发执行！')

    def onResetAllTasks(self):
        button = QMessageBox.question(self, '操作确认', '是否确认全部重置？重置后所有任务将触发重新执行！')
        if button == QMessageBox.StandardButton.Yes:
            self.cfgMgr.resetTasks()
            self.resetAllIcon()
            QMessageBox.information(self, '操作提示', '所有任务已重置成功！')

    def resetAllIcon(self):
        for i in range(self.list_todo.count()):
            item = self.list_todo.item(i)
            self.changeTaskIcon(iconType=IconTypeEnum.none, item=item)

    def onRemoveAllTasks(self):
        button = QMessageBox.question(self, '操作确认', '是否确认全部清空？')
        if button == QMessageBox.StandardButton.Yes:
            self.list_todo.clear()
            self.cfgMgr.removeAllTasks()

    def onRecommend(self):
        if self.list_todo.count() > 0:
            QMessageBox.critical(self, '操作提示', '待执行任务列表不为空，请先清空列表后再执行此操作。')
            return
        self.cfgMgr.loadRecommend()
        # 加载推荐配置时当日不再重置，避免出现直接自动关闭游戏情况
        self.cfgMgr.resetTasks(ignore=True)
        self.list_todo.clear()
        self.initTaskList()

        QMessageBox.information(self, '操作提示', '已成功加载推荐任务执行列表！')

    def onEditTask(self):
        task_name = self.list_todo.selectedItems()[0].text()
        task = self.cfgMgr.findTaskByName(task_name)
        option_dialog = TaskOptionDialog(task)
        if option_dialog.exec() == QDialog.DialogCode.Accepted:
            self.cfgMgr.saveTasks()

    def onFix(self):
        target_hwnd = gm_func.get_hwnd()
        if target_hwnd == 0:
            logging.info('未能获取到游戏窗口')
            return
        if self.check_top.isChecked():
            my_window.restore(target_hwnd)
            my_window.force_focus(target_hwnd)
        else:
            my_window.cancel_focus(target_hwnd)

    def onStatusChange(self, tp, msg):
        if tp == StatusTypeEnum.error:
            self.statusbar.setStyleSheet("color: rgb(229, 0, 0);")
        elif tp == StatusTypeEnum.success:
            self.statusbar.setStyleSheet("color: rgb(0, 170, 0);")
        elif tp == StatusTypeEnum.warn:
            self.statusbar.setStyleSheet("color: rgb(242, 131, 14);")
        else:
            self.statusbar.setStyleSheet("color: rgb(0, 159, 239);")
        self.statusbar.showMessage(msg)

    def onIconChange(self, tp, name):
        self.changeTaskIcon(name=name, iconType=tp, select=True)
