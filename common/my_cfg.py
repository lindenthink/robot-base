from enum import Enum
from json import load as json_load, dump as json_dump
from os import path
from datetime import datetime

from yaml import safe_load

import dirs
from common import my_util, my_window
from common.my_task import Task
from functools import lru_cache


@lru_cache(maxsize=32)
def loadMeta():
    with open(dirs.join_data('metadata.yml'), 'r', encoding='utf-8') as file:
        return safe_load(file)


class ConfigKey(Enum):
    args = 'args'
    args_mode = 'mode'
    tasks = 'tasks'
    resetDate = 'resetDate'
    single = 'single'


class ConfigManager:
    path = None
    cfg = None
    tasks = None
    args = None
    single = None

    def __init__(self, game='', user=''):
        self.game = game
        self.user = user
        self.path = path.join(my_util.baseDir(), f'{game}_{user}.cfg')
        self.load()

    def load(self):
        self.tasks = []
        if path.exists(self.path):
            with open(self.path, encoding='utf-8') as file:
                self.cfg = json_load(file)  # 返回dict对象
        else:
            self.cfg = {ConfigKey.tasks.value: [], ConfigKey.args.value: {ConfigKey.mode.value: my_window.MODE_FG},
                        ConfigKey.single.value: {}, ConfigKey.resetDate.value: my_util.fmtDate(datetime.now())}
        self.single = self.cfg[ConfigKey.single.value]
        self.args = self.cfg[ConfigKey.args.value]
        for item in self.cfg[ConfigKey.tasks.value]:
            task = Task(item)
            self.tasks.append(task)

    @lru_cache(maxsize=32)
    def loadRecommend(self):
        with open(dirs.join_data('recommend.json'), encoding='utf-8') as file:
            recommend_cfg = json_load(file)  # 返回dict对象
        self.tasks.clear()
        for item in recommend_cfg[ConfigKey.tasks.value]:
            task = Task(item)
            self.tasks.append(task)
        self.saveTasks()

    # 保存dict对象
    # @cost
    def saveTasks(self):
        self.cfg[ConfigKey.tasks.value] = self.tasks
        self.save(self.cfg)

    def save(self, content):
        with open(self.path, 'w', encoding='utf-8') as file:
            json_dump(content, file)

    def addTask(self, task_dict):
        task = Task(task_dict)
        self.tasks.append(task)
        self.saveTasks()

    def removeTask(self, name):
        for task in self.tasks:
            if task.name == name:
                self.tasks.remove(task)
                self.cfg[ConfigKey.tasks.value] = self.tasks
                self.saveTasks()
                break

    def removeAllTasks(self):
        self.tasks.clear()
        self.saveTasks()

    def resetTasks(self, ignore=False):
        if not ignore:
            for task in self.tasks:
                task.reset()
        self.cfg[ConfigKey.resetDate.value] = my_util.fmtDate(datetime.now())
        self.saveTasks()

    def resetTaskByName(self, name):
        for task in self.tasks:
            if task.name == name:
                task.reset()
                self.saveTasks()
                break

    def findTaskByName(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def succeedTask(self, name):
        for task in self.tasks:
            if task.name == name:
                task.succeed()
                self.saveTasks()
                break

    # 检查重置所有任务，每日首次执行时处理一次
    def checkReset(self):
        if ConfigKey.resetDate.name in self.cfg:
            reset_date = self.cfg[ConfigKey.resetDate.value]
            today = my_util.fmtDate(datetime.now())
            if reset_date == today:
                return False
        self.resetTasks()
        return True

    def updArg(self, argEnum, argValue):
        self.args[argEnum.value] = argValue
        self.cfg[ConfigKey.args.value] = self.args
        self.save(self.cfg)

    def getArg(self, argEnum):
        if argEnum.value in self.args:
            return self.args[argEnum.value]
        return None
