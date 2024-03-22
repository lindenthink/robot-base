from abc import abstractmethod

from gm import gm_func


class ITaskRunner:
    @abstractmethod
    def run(self, target=None, args=None, options=None):
        pass


class RestartRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.refresh_login(gm_func.get_hwnd(), mode=args['mode'])


class ThinkingRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.click_thinking(gm_func.get_hwnd(), mode=args['mode'])


class VisitorRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.click_visitor(gm_func.get_hwnd(), mode=args['mode'])


class RecvGiftRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.rec_gift(gm_func.get_hwnd(), mode=args['mode'])


class RecvMomentGiftRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.recv_moment_gift(gm_func.get_hwnd(), mode=args['mode'])


class TravelRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        count = options[0]['value']
        return gm_func.travel(hwnd=gm_func.get_hwnd(), count=count, mode=args['mode'])


class RecruitRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        accredit = options[0]['value']
        return gm_func.recruit(hwnd=gm_func.get_hwnd(), mode=args['mode'], accredit=accredit)


class StudyRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        collect_pills = options[0]['value']
        return gm_func.study(hwnd=gm_func.get_hwnd(), mode=args['mode'], collect_pills=collect_pills)


class AlchemyRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.alchemy_daily(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class ShareRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.share_game(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class RecvTowerGiftRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        sweep = options[0]['value']
        return gm_func.tower_gift(hwnd=gm_func.get_hwnd(), mode=args['mode'], sweep=sweep)


class BreakThroughRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        take_medicine = options[0]['value']
        return gm_func.breakthrough(hwnd=gm_func.get_hwnd(), mode=args['mode'], take_medicine=take_medicine)


class DemonFightRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        is_triple = options[0]['value']
        return gm_func.demon(hwnd=gm_func.get_hwnd(), mode=args['mode'], is_triple=is_triple)


class BossFightRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        qualities = options[0]['value']
        types = options[1]['value']
        return gm_func.task_boss(hwnd=gm_func.get_hwnd(), mode=args['mode'], qualities=qualities, types=types)


class UnionAssistRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        # 最后一次触发膜拜
        worship = options[0]['value']
        if worship:
            worship = target.todoCount == (target.doneCount + 1)
        return gm_func.union_assist(hwnd=gm_func.get_hwnd(), mode=args['mode'], worship=worship)


class RewardRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        stars = options[0]['value']
        use_ticket = options[1]['value']
        pay_fresh = options[2]['value']
        rebel_first = options[3]['value']
        only_rebel = options[4]['value']
        return gm_func.reward(hwnd=gm_func.get_hwnd(), mode=args['mode'], stars=stars, use_ticket=use_ticket,
                              pay_refresh=pay_fresh, rebel_first=rebel_first, only_rebel=only_rebel)


class ZhenYaoRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.zhenyaojian(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class MineRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        concurrent = options[0]['value']
        return gm_func.mine(hwnd=gm_func.get_hwnd(), mode=args['mode'], concurrent=concurrent)


class RecvChessGiftRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        recv_range = options[0]['value']
        return gm_func.chess_gift(hwnd=gm_func.get_hwnd(), mode=args['mode'], recv_range=recv_range)


class MasterSkillRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.use_master_skill(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class MasterBreakthroughRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.check_master_breakthrough(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class MasterSkillBreakthroughRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.check_master_skill(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class UnionHongbaoRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.union_hongbao(hwnd=gm_func.get_hwnd(), mode=args['mode'])


class LinkMineRunner(ITaskRunner):
    def run(self, target=None, args=None, options=None):
        return gm_func.link_mine(hwnd=gm_func.get_hwnd(), mode=args['mode'])


runners = {
    '重启': RestartRunner(),
    '心事': ThinkingRunner(),
    '访客': VisitorRunner(),
    '游历': TravelRunner(),
    '日常炼丹': AlchemyRunner(),
    '藏经阁研习': StudyRunner(),
    '招收弟子': RecruitRunner(),
    '分享游戏': ShareRunner(),
    '领取锁妖塔灵石': RecvTowerGiftRunner(),
    '礼包领取': RecvGiftRunner(),
    '游戏圈礼包领取': RecvMomentGiftRunner(),
    '购买魂殿礼包': RecvChessGiftRunner(),
    '突破': BreakThroughRunner(),
    '妖王': DemonFightRunner(),
    '妖窟': BossFightRunner(),
    '红包': UnionHongbaoRunner(),
    '协助': UnionAssistRunner(),
    '悬赏': RewardRunner(),
    '镇妖涧': ZhenYaoRunner(),
    '挖矿': MineRunner(),
    '掌门功法使用': MasterSkillRunner(),
    '掌门修为突破': MasterBreakthroughRunner(),
    '掌门功法升级': MasterSkillBreakthroughRunner(),
}
