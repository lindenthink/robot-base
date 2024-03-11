from PyQt6.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QPushButton,\
    QLabel, QSpinBox, QDateTimeEdit, QCheckBox, QComboBox, QVBoxLayout

from common import my_util
from common.my_task import TaskTypeEnum


class TaskOptionDialog(QDialog):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setWindowTitle('选项配置')
        self.setFixedSize(300, 320)
        self.form = QFormLayout()
        self.setLayout(self.form)

        self.nameLabel = QLabel()
        self.nameLabel.setStyleSheet('color: grey;')
        self.nameLabel.setText(task.name)
        self.form.addRow('任务名称：', self.nameLabel)

        self.stateLabel = QLabel()
        self.stateLabel.setStyleSheet('color: grey;')
        self.stateLabel.setText(task.stateName())
        self.form.addRow('当前状态：', self.stateLabel)

        self.typeLabel = QLabel()
        self.typeLabel.setStyleSheet('color: grey;')
        self.typeLabel.setText(task.typeName())
        self.form.addRow('执行方式：', self.typeLabel)

        if task.todoCount is not None:
            self.todoCountInput = QSpinBox()
            if task.type == TaskTypeEnum.schedule.value or task.type == TaskTypeEnum.immediate.value:
                self.todoCountInput.setEnabled(False)
            self.todoCountInput.setValue(task.todoCount)
            self.form.addRow('执行次数：', self.todoCountInput)

        if task.type == TaskTypeEnum.interval.value:
            self.intervalInput = QSpinBox()
            self.intervalInput.setMaximum(1800)
            self.intervalInput.setSingleStep(5)
            self.intervalInput.setValue(task.interval)
            self.form.addRow('间隔分钟：', self.intervalInput)
            self.nextTimeLabel = QLabel()
            self.nextTimeLabel.setStyleSheet('color: grey;')
            self.nextTimeLabel.setText(task.nextTime)
            self.form.addRow('下次执行：', self.nextTimeLabel)
        elif task.type == TaskTypeEnum.schedule.value:
            self.scheduleInput = QDateTimeEdit(my_util.parseTime(task.nextTime))
            self.scheduleInput.setDisplayFormat('HH:mm')
            self.form.addRow('执行时间：', self.scheduleInput)

        self.doneCountLabel = QLabel()
        self.doneCountLabel.setStyleSheet('color: grey;')
        self.doneCountLabel.setText(f'{task.doneCount}')
        self.form.addRow('完成次数：', self.doneCountLabel)

        # 处理选项
        if task.options is not None:
            i = 0
            for option in task.options:
                i += 1
                op_name = f'op{i}'
                tmp = None
                op_type = option['type']
                op_val = option['value']
                if op_type == 'num':
                    tmp = QSpinBox()
                    tmp.setValue(op_val)
                elif op_type == 'bool':
                    tmp = QCheckBox()
                    tmp.setChecked(op_val)
                elif op_type == 'checklist':
                    tmp = QVBoxLayout()
                    j = 0
                    for item in option['items']:
                        # 每行两个选项，过多会挤到一起
                        if j % 2 == 0:
                            tmp_layout = QHBoxLayout()
                            tmp.addItem(tmp_layout)
                        tmp_item = QCheckBox()
                        tmp_item.setText(item)
                        tmp_item.setChecked(item in option['value'])
                        item_name = f'{op_name}_item{j}'
                        tmp_layout.addWidget(tmp_item)
                        setattr(self, item_name, tmp_item)
                        j += 1
                elif op_type == 'select':
                    tmp = QComboBox()
                    for item in option['items']:
                        tmp.addItem(item)
                    tmp.setCurrentIndex(op_val)
                self.form.addRow(f'{option["name"]}：', tmp)

                if 'desc' in option:
                    descLabel = QLabel()
                    descLabel.setStyleSheet("color: red;")
                    descLabel.setWordWrap(True)
                    descLabel.setText(option['desc'])
                    self.form.addRow('', descLabel)
                setattr(self, op_name, tmp)

        if task.notice is not None:
            self.noticeLabel = QLabel()
            self.noticeLabel.setStyleSheet("color: red;")
            self.noticeLabel.setWordWrap(True)
            self.noticeLabel.setText(task.notice)
            self.form.addRow('特别说明：', self.noticeLabel)

        btn_box = QHBoxLayout()
        self.okBtn = QPushButton('确认', self)
        btn_box.addWidget(self.okBtn)
        self.okBtn.clicked.connect(self.ok)
        self.cancelBtn = QPushButton('取消', self)
        btn_box.addWidget(self.cancelBtn)
        self.cancelBtn.clicked.connect(self.close)
        self.form.addRow(btn_box)

    def ok(self):
        if self.task.todoCount is not None:
            self.task.todoCount = self.todoCountInput.value()
        if self.task.type == TaskTypeEnum.interval.value:
            self.task.interval = self.intervalInput.value()
        elif self.task.type == TaskTypeEnum.schedule.value:
            self.task.nextTime = self.scheduleInput.text()

        if self.task.options is not None:
            i = 0
            for option in self.task.options:
                i += 1
                op_name = f'op{i}'
                op_type = option['type']
                tmp = getattr(self, op_name)
                if op_type == 'num':
                    option['value'] = tmp.value()
                elif op_type == 'bool':
                    option['value'] = tmp.isChecked()
                elif op_type == 'checklist':
                    option['value'] = []
                    for j in range(0, len(option['items'])):
                        item_name = f'{op_name}_item{j}'
                        tmp_item = getattr(self, item_name)
                        if tmp_item.isChecked():
                            option['value'].append(tmp_item.text())
                elif op_type == 'select':
                    option['value'] = tmp.currentIndex()
        self.accept()
