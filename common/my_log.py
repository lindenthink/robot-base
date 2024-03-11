from logging import Handler


class TextEditLogHandler(Handler):
    def __init__(self, emitLog):
        Handler.__init__(self)
        self.emitLog = emitLog

    def emit(self, record):
        msg = self.format(record)
        # 此处仅触发记录日志信号，直接记录会导致程序崩溃，参考：https://blog.csdn.net/qq_38141255/article/details/125658868
        self.emitLog(msg)
