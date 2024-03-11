import logging
from sys import argv as sys_argv, exit as sys_exit

from PyQt6.QtWidgets import QApplication

import ui.MainWindow as MainWindow
from common.my_log import TextEditLogHandler


def main():
    app = QApplication(sys_argv)
    main_window = MainWindow()
    textEditHandler = TextEditLogHandler(main_window.emitLog)
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, datefmt='[%Y-%m-%d %H:%M:%S]',
                        handlers=[textEditHandler, logging.StreamHandler()])
    sys_exit(app.exec())


if __name__ == '__main__':
    main()
