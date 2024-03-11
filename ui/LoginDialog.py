from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, \
    QHBoxLayout, QFormLayout, QButtonGroup, QRadioButton, QMessageBox
import common.my_service as service
from ui.service import LoginInfo


class LoginDialog(QDialog):

    def __init__(self, loginInfo):
        super().__init__()

        self.login_info: LoginInfo = loginInfo
        self.setWindowTitle(f'菩提思 | { self.login_info.gmName}')
        self.setFixedSize(280, 200)

        self.form = QFormLayout()
        self.setLayout(self.form)

        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText('请输入账号')
        self.nameInput.setMaxLength(32)
        self.nameInput.textChanged.connect(self.onCheckInput)
        self.form.addRow('账号', self.nameInput)

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入密码')
        self.pwdInput.setMaxLength(32)
        self.pwdInput.textChanged.connect(self.onCheckInput)
        self.pwdInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.form.addRow('密码', self.pwdInput)

        radio_box = QHBoxLayout()
        radio_group = QButtonGroup()
        self.radio_login = QRadioButton('登陆')
        self.radio_login.setChecked(True)
        self.op = '登陆'
        self.radio_login.clicked.connect(self.onChooseRadio)
        self.radio_reg = QRadioButton('注册')
        self.radio_reg.clicked.connect(self.onChooseRadio)
        radio_group.addButton(self.radio_login)
        radio_group.addButton(self.radio_reg)
        radio_box.addWidget(self.radio_login)
        radio_box.addWidget(self.radio_reg)
        self.form.addRow('操作类型', radio_box)

        self.warnLabel = QLabel('', self)
        self.warnLabel.setStyleSheet('color:red')
        self.form.addRow('', self.warnLabel)

        btn_box = QHBoxLayout()
        self.loginBtn = QPushButton('确认', self)
        self.loginBtn.clicked.connect(self.onConfirm)
        btn_box.addWidget(self.loginBtn)

        self.cancelBtn = QPushButton('取消', self)
        self.cancelBtn.clicked.connect(self.close)
        btn_box.addWidget(self.cancelBtn)
        self.form.addRow('', btn_box)

    def onConfirm(self):
        if not self.onCheckInput():
            return
        input_name = self.nameInput.text()
        input_pwd = self.pwdInput.text()
        if self.op == '登陆':
            res = service.login(input_name, input_pwd, game=self.login_info.gmCode, ver=self.login_info.gmVer)
            if res['code'] != 1:
                self.warn(res['message'])
                return
            self.login_info.username = input_name
            self.login_info.password = input_pwd
            self.login_info.encKey = res['data']['encKey']
            self.login_info.expireTime = res['data']['expireTime']
            self.accept()
        else:
            res = service.register(input_name, input_pwd, game=self.login_info.gmCode)
            if res['code'] != 1:
                self.warn(res['message'])
                return
            QMessageBox.information(self, '提示', '注册成功，请登陆！', QMessageBox.StandardButton.Ok)
            self.pwdInput.setText('')
            self.radio_login.click()

    def onCheckInput(self):
        input_name = self.nameInput.text()
        if input_name is None or input_name == '':
            self.warn('用户名不能为空')
            return False
        if len(input_name) < 6:
            self.warn('用户名长度不小于6')
            return False

        input_pwd = self.pwdInput.text()
        if input_pwd is None or input_pwd == '':
            self.warn('密码不能为空')
            return False
        if len(input_pwd) < 6:
            self.warn('密码长度不小于6')
            return False

        if self.radio_login.isChecked():
            self.warn('')
            return True

        confirm_pwd = self.pwdConfirmInput.text()
        if input_pwd != confirm_pwd:
            self.warn('两次输入密码不一致')
            return False
        self.warn('')
        return True

    def onChooseRadio(self):
        sender = self.sender()
        new_op = sender.text()
        if self.op == new_op:
            return

        self.op = new_op
        if new_op == '注册':
            self.pwdConfirmInput = QLineEdit()
            self.pwdConfirmInput.setPlaceholderText('请再次输入密码')
            self.pwdConfirmInput.setEchoMode(QLineEdit.EchoMode.Password)
            self.pwdConfirmInput.textChanged.connect(self.onCheckInput)
            self.form.insertRow(2, '确认密码', self.pwdConfirmInput)
        else:
            self.form.removeRow(2)

    def warn(self, msg: str):
        self.warnLabel.setText(msg)
