from datetime import datetime
import logging
from enum import Enum

from common import my_util
from gm.gm_runner import runners


class TaskTypeEnum(Enum):
    cycle = -1
    immediate = 0
    interval = 1
    schedule = 2


class TaskStateEnum(Enum):
    init = 0
    doing = 1
    done = 2


class Task(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def _canDo(self):
        if self.state == TaskStateEnum.done.value:  # 注意不能直接使用Enum
            return False
        if self.type == TaskTypeEnum.interval.value:
            return self.nextTime is None or my_util.fmtDateTime() >= self.nextTime
        # 兼容循环执行设置首次执行时间
        return self.nextTime is None or my_util.fmtTime() >= self.nextTime

    def isDone(self):
        return TaskStateEnum.done.value == self.state

    def run(self, args=None):
        if self.name not in runners:
            logging.info(f'忽略处理<{self.name}>，该任务无效请进行删除')
            self.state = TaskStateEnum.done.value
            return False
        runner = runners[self.name]
        if self.isDone():
            return True
        if not self._canDo():
            return False
        if self.type != TaskTypeEnum.cycle.value:
            logging.info(f'开始执行{self.name}')
        try:
            success = runner.run(target=self, args=args, options=self.options)
            if not success:
                return False
        except Exception as e:
            logging.error(e)
            return False
        self.doneCount += 1
        if self.doneCount == self.todoCount:
            self.state = TaskStateEnum.done.value
        elif self.type == TaskTypeEnum.interval.value:
            next_time = my_util.addMinutes(date=datetime.now(), minutes=self.interval)
            self.nextTime = my_util.fmtDateTime(next_time)
        logging.info(f'{self.name}执行完成，累计成功{self.doneCount}次')
        return True

    def reset(self):
        self.state = TaskStateEnum.init.value
        self.doneCount = 0
        if self.type == TaskTypeEnum.interval.value:
            self.nextTime = None

    def succeed(self):
        self.state = TaskStateEnum.done.value

    def typeName(self):
        if self.type == TaskTypeEnum.cycle.value:
            return '循环执行'
        elif self.type == TaskTypeEnum.interval.value:
            return '间隔执行'
        elif self.type == TaskTypeEnum.schedule.value:
            return '定时执行'
        return '立即执行'

    def stateName(self):
        if self.state == TaskStateEnum.done.value:
            return '已完成'
        elif self.doneCount > 0:
            return '执行中'
        return '待执行'
