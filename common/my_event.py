from PyQt6.QtCore import QThread
from pynput import mouse


class MouseListener(QThread):
    listener = None
    on_click = None
    on_move = None

    def __init__(self, on_click, on_move):
        super().__init__()
        self.on_click = on_click
        self.on_move = on_move

    def run(self):
        self.listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.listener.start()
        self.listener.join()

    def stop(self):
        if self.listener.is_alive():
            self.listener.stop()
