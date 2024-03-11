from abc import abstractmethod

from gm import gm_func


class ITaskRunner:
    @abstractmethod
    def run(self, target=None, args=None, options=None):
        pass


class RestartRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.refresh(gm_func.get_hwnd(), mode=args['mode'])


runners = {
    '重启': RestartRunner(),
}
