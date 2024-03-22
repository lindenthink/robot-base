from os import path
import dirs


'''
路径
'''
# 图片根路径
PATH_IMG = dirs.join_template('gm')


def join(name):
    return path.join(PATH_IMG, f'{name}.jpg')


# 主窗口
ID_MAIN_VIEW = join('id_main_view')

# 公告
ID_NOTICE = join('id_notice')
# 公告-未读
ID_NOTICE_UNREAD = join('id_notice_unread')
ID_NOTICE_UNREAD2 = join('id_notice_unread2')
# 离线收益
ID_OFFLINE_INCOME = join('id_offline_income')

# 免费广告
ID_AD_FREE = join('id_ad_free')
# 时幻沙
ID_TIME_SAND = join('id_time_sand')

# 游历-窗口
ID_TRAVEL_VIEW = join('id_travel_view')
# 游历—免费
ID_TRAVEL_FREE = join('id_travel_free')
# 游历-快速收益
BTN_TRAVEL_QUICK_1 = join('btn_travel_quick_1')
# 游历-快速收益-领取
BTN_TRAVEL_QUICK_2 = join('btn_travel_quick_2')
# 回城
BTN_BACK_CITY = join('btn_back_city')

# 招募对话
ID_RECRUIT_VIEW = join('id_recruit_view')

# 退出提示
ID_EXIT_HINT = join('id_exit_hint')

# 无法通行
ID_NO_ENTRY = join('id_no_entry')

# 倍速
ID_SPEED = join('id_speed')
# 三倍速
ID_TRIPLE = join('id_triple')

# 箭头指示建筑位置
ID_POINTING = join('id_pointing')

# 红色感叹号
ID_COMMA = join('id_comma')

# 锁妖塔免费扫荡
ID_TOWER_GIFT_FREE = join('id_tower_gift_free')

# 章节奖励
ID_CHAPTER_REWARD = join('id_chapter_reward')

# 立即完成
ID_RIGHT_FINISH = join('id_right_finish')

'''
斗技
'''
ID_DOUJI_HOME = join('id_douji_home')
ID_DOUJI_TIAOZHAN = join('id_douji_tiaozhan')
# 斗技结束
ID_DOUJI_FINISHED = join('id_douji_finished')


'''
BOSS
'''
# 妖窟不存在
ID_BOSS_NONE = join('id_boss_none')
# 人数上线
ID_BOSS_FULL = join('id_boss_full')
# 结算奖池
ID_BOSS_JIANGCHI = join('id_boss_jiangchi')
# 镇魔令
ID_BOSS_TICKET = join('id_boss_ticket')
# 战斗界面
ID_BOSS_FIGHT = join('id_boss_fight')
# 参战
ID_BOSS_JOIN = join('id_boss_join')
# 讨伐
ID_BOSS_TAOFA_LIST = [join('id_boss_taofa'), join('id_boss_taofa2')]
# 讨伐-2
ID_BOSS_TAOFA_2 = join('id_boss_taofa_2')
# 协战
ID_BOSS_XIEZHAN = join('id_boss_xiezhan')
# 协战-2
ID_BOSS_XIEZHAN_2 = join('id_boss_xiezhan_2')
# 妖窟
ID_BOSS_YAOKU = join('id_boss_yaoku')
# 抽奖
ID_BOSS_CHOUJIANG = join('id_boss_choujiang')
# 战斗界面退出，和已有的退出按钮匹配不上
ID_BOSS_EXIT = join('id_boss_exit')
BOSS_QUALITIES = {'难': 'hard', '中': 'mid'}
BOSS_TYPES = {'鸟': 'bird', '凤': 'phoenix', '蛇': 'snake', '蟹': 'crab', '鱼': 'fish'}

# 镇妖涧-剩余0次
ID_ZHENYAO_NONE = join('id_zhenyao_none')

# 分享的logo
ID_SHARE_LOGOS = [join('id_share_logo1'), join('id_share_logo2')]

# 月卡领取
BTN_MCARD_REC = join('btn_mcard_rec')
# 礼包-机缘-供奉-已领取
ID_GONGFENG_RECEIVED = join('id_gongfeng_received')
# 广告
BTN_GIFT_AD_PLAY = join('btn_gift_ad_play')
# 日礼包-100
ID_GIFT_DAILY_CHESS = join('id_gift_daily_chess')
# 每日特惠
BTN_GIFT_DISPOSABLE = join('btn_gift_disposable')

# 心事
BTN_THINKING = join('btn_thinking')
# 心事-弟子位置
BTN_THINKING_2 = join('btn_thinking_2')

# 对话进行中
ID_TALKING = [join('id_talking_visitor'), join('id_talking_thinking')]

# 建筑明细界面
ID_BUILDING_DETAIL = join('id_building_detail')

# 获得
ID_ACQUIRE = join('id_acquire')

# 建筑明细界面
ID_ZHAOMU = join('id_zhaomu')

# 仙盟-主界面
ID_UNION_VIEW = join('id_union_view')
# 仙盟-协助
BTN_UNION_ASSIST = join('btn_union_assist')
# 仙盟-红包
ID_UNION_HONGBAO = join('id_union_hongbao')
# 仙盟-膜拜-未指派仙尊
ID_UNION_WORSHIP_EMPTY = join('id_union_worship_empty')
# 确认
BTN_CONFIRM = join('btn_confirm')

# 访客
BTN_VISITOR = join('btn_visitor')
# 访客-问号
BTN_VISITOR_2 = join('btn_visitor_2')
# 访客-风灵月影战斗
BTN_VISITOR_FIGHT = join('btn_visitor_fight')
# 访客-需要确认的选项集合
BTN_VISITOR_OPTIONS = [join('btn_visitor_option_1'),
                       join('btn_visitor_option_2'),
                       join('btn_visitor_option_3'),
                       join('btn_visitor_option_4'),
                       join('btn_visitor_option_5'),
                       join('btn_visitor_option_6'),
                       join('btn_visitor_option_7'),
                       ]
# 更新断连
BTN_UPDATE_REENTRY = join('btn_update_reentry')
BTN_UPDATE_REENTRY2 = join('btn_update_reentry2')
# 更新重试
BTN_UPDATE_RETRY = join('btn_update_retry')
# 被顶下线
ID_OCCUPY_OFFLINE = join('id_occupy_offline')
# 断连重试
BTN_OFFLINE_RETRY = join('btn_offline_retry')

# 聊天框
BTN_CHAT = join('btn_chat')

# 挑战
BTN_TIAOZHAN = join('btn_tiaozhan')

# 退出按钮
BTN_EXIT = join('btn_exit')

# 撤退
BTN_RETREAT = join('btn_retreat')

# 批量招收划开后的逐个招收按钮
BTN_RECRUIT = join('btn_recruit')

# 提示研习按钮
BTN_STUDY = join('btn_study')

'''
魂殿礼包
'''
# 坐标-棋局
LOC_CHESS = (420, 260)
# 魂殿入口，等级低的没有机缘商店
ID_CHESS_ENTRY = join('id_chess_entry')
# 魂殿礼包集合
CHESS_GIFTS = {'万能魂石': join('chess_gift_wanneng'), '挑战令': join('chess_gift_tiaozhan'),
               '鹿矫灵仙芝': join('chess_gift_lingzhi'), '轮回异宝箱': join('chess_gift_yibao'),
               '艮岳景观匣': join('chess_gift_genyue'), '红色招募令': join('chess_gift_zhaomu'),
               '十万年金雷竹':join('chess_gift_hongzhu'), '丹材': join('chess_gift_dancai'),
                }

'''
炼丹
'''
# 炼丹成功
BTN_ALCHEMY_FINISH = join('btn_alchemy_finish')
# 炼丹中
ID_ALCHEMY_EMPTY = join('id_alchemy_empty')
# 主界面炼丹成功提示
BTN_ALCHEMY_PROMPT = join('btn_alchemy_prompt')

'''
突破
'''
# 弟子面板
ID_DISCIPLE_VIEW = join('id_disciple_view')
# 破镜/突破/渡劫
BTN_BREAKTHROUGH_TODO = [join('btn_breakthrough_1'), join('btn_breakthrough_2'), join('btn_breakthrough_3')]
# 突破结果
ID_BREAKTHROUGH_RESULT = [join('id_breakthrough_success'), join('id_breakthrough_success_2'),
                          join('id_breakthrough_fail'), join('id_breakthrough_fail_2')]
# 突破结果-触发突破动画需要两次退出
ID_BREAKTHROUGH_RESULT_EXIT_TWICE = [join('id_breakthrough_success'), join('id_breakthrough_fail')]
# 轮回
ID_DISCIPLE_LUNHUI = join('id_disciple_lunhui')
# 奇才
ID_DISCIPLE_QICAI = join('id_disciple_qicai')
# 快速派驻
ID_DISCIPLE_QUICK_STATION = join('id_disciple_quick_station')
# 被指导
ID_GUIDED = join('id_guided')
# 不吃药标识
ID_BREAKTHROUGH_NO_MEDICINE = join('id_breakthrough_no_medicine')
# 弟子感叹号
ID_DISCIPLE_COMMA = join('id_disciple_comma')
# 不记名弟子
ID_DISCIPLE_TMP = join('id_disciple_tmp')

'''
日常任务
'''
# 标识-任务列表
ID_TASKLIST = join('id_tasklist')
# 标识-任务未执行
ID_TASK_TODO = join('id_task_todo')
# 礼包退出
BTN_GIFT_EXIT = join('btn_gift_exit')
# 标识-售罄
ID_GIFT_AD_SELLOUT = join('id_gift_ad_sellout')

'''
悬赏
'''
# 悬赏令牌
ID_REWARD_TICKET = join('id_reward_ticket')
# 悬赏-任务星数列表
ID_REWARD_STAR_LIST = [join('id_reward_2stars'), join('id_reward_3stars'), join('id_reward_4stars'),
                       join('id_reward_5stars'), join('id_reward_6stars')]
# 悬赏-反贼任务
ID_REWARD_REBEL = join('id_reward_rebel')
# 悬赏-免费刷新
ID_REWARD_REFRESH_FREE = join('id_reward_refresh_free')
# 悬赏-空任务
ID_REWARD_EMPTY = join('id_reward_empty')
# 悬赏-可接取
ID_REWARD_TODO = join('id_reward_todo')
# 悬赏-待委派
ID_REWARD_NO_WORKER = join('id_reward_no_worker')
# 悬赏-协助
ID_REWARD_ASSIST = join('id_reward_assist')

'''
坐标
'''
# 坐标-礼包
LOC_GIFT = (420, 310)
# 坐标-礼包-退出
LOC_GIFT_EXIT = (405, 800)

# 坐标-月卡-天缘令
LOC_GIFT_MONTH_1 = (270, 340)
# 坐标-月卡-天机令
LOC_GIFT_MONTH_2 = (270, 575)

# 坐标-日礼包
LOC_GIFT_DAILY = (175, 775)
# 坐标-日礼包-免费
LOC_GIFT_DAILY_0 = (155, 195)
# 坐标-日礼包-100机缘
LOC_GIFT_DAILY_100 = (375, 315)

# 坐标-周礼包
LOC_GIFT_WEEKLY = (245, 775)
# 坐标-周礼包-免费
LOC_GIFT_WEEKLY_0 = (155, 195)
# 坐标-周礼包-300机缘
LOC_GIFT_WEEKLY_300 = (375, 195)
# 坐标-周礼包-500机缘
LOC_GIFT_WEEKLY_500 = (155, 315)

# 坐标-福礼阁
LOC_GIFT_AD = (330, 775)

# 坐标-礼包-机缘
LOC_GIFT_JIYUAN = (40, 775)
# 坐标-礼包-机缘-玄象阁
LOC_GIFT_JIYUAN_STEP1 = (80, 600)
# 坐标-礼包-机缘-玄象阁-每日馈赠
LOC_GIFT_JIYUAN_STEP2 = (170, 110)
# 坐标-礼包-机缘-玄象阁-每日馈赠-一键领取
LOC_GIFT_JIYUAN_STEP3 = (365, 630)

# 坐标-建造
LOC_BUILD = (40, 780)

# 坐标-弟子
LOC_DISCIPLE = (115, 780)

# 坐标-任务
LOC_TASK = (195, 780)

# 坐标-仙盟
LOC_UNION = (270, 780)
# 坐标-游历
LOC_TRAVEL = (380, 765)
# 坐标-斗技
LOC_CONTEND = (420, 420)

# 文本框坐标
LOC_TEXT = (100, 415)
# 文本框框-完成按钮坐标
LOC_TEXT_FINISH = (165, 475)

# 确定看广告坐标
LOC_AD_CONFIRM = (315, 525)

'''
铸炼
'''
ID_ZHULIAN_VIEW = join('id_zhulian_view')
ID_ZHULIAN_EMPTY = join('id_zhulian_empty')
# 快速铸造
BTN_QUICK_ZHULIAN = join('btn_quick_zhulian')
# 铸炼中
ID_ZHULIAN_ING = join('id_zhulian_ing')
# 铸炼-未分配弟子
ID_ZHULIAN_NO_WORKER = join('id_zhulian_no_worker')
# 铸炼坐标
LOC_ZHULIAN_1 = (240, 340)
# 图纸类型2(衣服)
LOC_ZHULIAN_TYPE_2 = (90, 360)
# 图纸类型3(佩)
LOC_ZHULIAN_TYPE_3 = (90, 445)
# 选择图纸
LOC_ZHULIAN_TYPE_SELECT = (250, 610)
# 图纸等级8坐标
LOC_ZHULIAN_LEVEL_8 = (365, 675)
# 铸炼坐标
LOC_ZHULIAN_2 = (220, 770)
# 确认铸炼
LOC_ZHULIAN_CONFIRM = (225, 555)

'''
挖矿
'''
ID_MINE_NONE = join('id_mine_none')
ID_MINE_FINISHED = join('id_mine_finished')
ID_MINE_EMPTY = join('id_mine_empty')
ID_MINE_SEAT = join('id_mine_seat')
# 矿石
ID_MINE_ORE = join('id_mine_ore')
# 占领提示矿锄不足
ID_MINE_LACK_OCCUPY = join('id_mine_lack_occupy')
# 刷新提示矿锄不足
ID_MINE_LACK_REFRESH = join('id_mine_lack_refresh')

'''
妖王
'''
# 微信聊天-妖王
ID_DEMON_WX = join('id_demon_wx')
# 妖王-已消失
ID_DEMON_NULL = join('id_demon_null')
# 妖王/仙盟boss副本内
ID_DEMON_FIGHT = join('id_demon_fight')

'''
掌门功法
'''
# 可使用
ID_MASTER_SKILL_CANUSE = join('id_master_skill_canuse')
# 斗转星移
ID_MASTER_SKILL_STAR = join('id_master_skill_star')
# 呼风唤雨
ID_MASTER_SKILL_RAIN = join('id_master_skill_rain')

'''
掌门突破
'''
# 掌门界面
ID_MASTER_VIEW = join('id_master_view')
# 掌门突破
ID_MASTER_BREAKTHROUGH = join('id_master_breakthrough')
# 掌门功法突破
ID_MASTER_SKILL_BREAKTHROUGH = join('id_master_skill_breakthrough')
# 掌门破镜/突破/渡劫
BTN_MASTER_BREAKTHROUGH_TODO = [join('btn_master_breakthrough_1'), join('btn_master_breakthrough_2'),
                                join('btn_master_breakthrough_3')]
# 掌门功法-修炼圆满
ID_MASTER_SKILL_FULL = join('id_master_skill_full')
# 掌门功法-解封
ID_MASTER_SKILL_UNSEAL = join('id_master_skill_unseal')

'''
限时活动
'''
# 联动入口
ID_LINK_ENTRY = join('id_link_entry')
# 矿脉探索
ID_LINK_EXPLORE = join('id_link_explore')
# 矿脉可探索
ID_LINK_MINE_EMPTY = join('id_link_mine_empty')
# 矿脉结束
ID_LINK_END = join('id_link_end')
