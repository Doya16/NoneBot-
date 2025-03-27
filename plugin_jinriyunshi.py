from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.rule import to_me
from nonebot_plugin_apscheduler import scheduler

import random
import os
import json
import datetime

# 指令初始化
from nonebot import on_message

def yunshi_rule(event: MessageEvent) -> bool:
    text = event.get_plaintext().strip()
    return text.startswith(".今日人品") or text.startswith(".今日运势")


yunshi_cmd = on_message(rule=yunshi_rule, priority=10, block=True)

# 路径与缓存
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
CACHE_PATH = os.path.join(CACHE_DIR, "daily_cache.json")

# 创建 cache 文件夹
os.makedirs(CACHE_DIR, exist_ok=True)

# 加载缓存
def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(data):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

today_cache = load_cache()
today_date = datetime.date.today().isoformat()

# 每日清空缓存
@scheduler.scheduled_job("cron", hour=0, minute=0)
def reset_cache():
    global today_cache, today_date
    today_cache = {}
    today_date = datetime.date.today().isoformat()
    save_cache(today_cache)

# 文案嵌入
YUNSHI_DATA = {
    0: {"title": "渊厄（深渊级厄运）", "texts": [
        "黑云蔽日戾气生，妄动恐遭意外横\n避讼远行皆不宜，谨言慎行待阳升\n宜守本心持斋戒，可化七成劫厄功",
        "天狗食月星斗沉，三尸作祟乱神魂\n钱财莫过他人手，饮食当防异物侵\n静诵黄庭三百字，或得仙真护命门",
        "六爻俱凶卦象危，白虎临宫血光随\n大事勿决缓三日，急病速医莫迟疑\n幸有贵人东北至，赠符一道解重围"
    ]},
    1: {"title": "坎陷（坎卦级险境）", "texts": [
        "如履薄冰临深渊，暗流涌动危机藏\n投资合作需明辨，情爱莫信蜜语甜\n幸得玄武暗中佑，慎终如始可渡关",
        "迷雾锁江舟难行，小人作祟是非生\n重要文书反复核，签约宜择戌时成\n随身佩玉挡灾煞，紫气东来运渐明",
        "命犯卷舌多口舌，无心快语惹风波\n晨起面向正南拜，朱雀化吉福自多\n戌狗属相宜相助，转危为机看谋略"
    ]},
    2: {"title": "陷厄（沉陷级困局）", "texts": [
        "丧门照命阴霾生，破财失物忌远行\n卯时莫饮无名水，辰刻慎接陌生盟\n幸有戌狗生肖客，赠赤玉髓挡灾星",
        "病符侵体气运低，寒热失调饮食忌\n西南方位莫久留，铜钱红线锁元气\n亥时焚艾净宅后，可引天医去顽疾",
        "勾陈盘踞是非缠，流言蜚语如箭穿\n巳时莫论他人过，未刻休辩钱财缘\n贵人隐在正东位，青衫老者指迷玄"
    ]},
    3: {"title": "蹇难（蹇卦级阻滞）", "texts": [
        "天罗地网困蛟龙，文书契约藏刀锋\n重大决策延七日，情感纠葛暂装聋\n午时面西拜白虎，铜铃三响破樊笼",
        "五鬼运财反噬凶，偏门财路终成空\n子夜门窗须锁紧，寅时异响莫追踪\n速请桃木刻鼠相，置于乾位镇邪祟",
        "驿马倒悬行路难，舟车易误机改签\n随身携带五谷袋，遇险默念井卦言\n东北忽现双鹊舞，便是厄尽祥瑞显"
    ]},
    4: {"title": "中正（平衡之境）", "texts": [
        "阴阳和合万物生，寒暑相推运道平\n守成胜过冒然进，持盈保泰即功成\n偶见虹霓贯东西，静待时机自有凭",
        "太极流转归浑元，无咎无誉最安然\n晨练宜择卯时起，投资可选土属性\n忽闻故人传佳讯，笑谈往昔续前缘",
        "星斗循轨各司职，春种秋收循旧例\n创新之事且三思，传统领域有机遇\n酉时得见双飞燕，或是吉兆隐天机"
    ]},
    5: {"title": "渐吉（渐进式祥兆）", "texts": [
        "三合局成运道开，旧债清偿新财来\n辰时宜种招财竹，申刻可试小量投\n红鸾星影初显现，含蓄回应方为优",
        "文昌熠熠照文曲，考证竞试正当时\n巳时沐浴更衣冠，朱砂点额增灵智\n西方偶遇捧书客，三问玄机得妙思",
        "玉堂贵人暗中扶，陈年恩怨今日无\n失物重现巽方位，故友传讯解心枯\n酉时备酒待客至，可得商机藏卦图"
    ]},
    6: {"title": "通明（通达级吉运）", "texts": [
        "禄存高照财门开，冷灶忽现贵人柴\n巳时签约利三倍，午刻投资翻番来\n切记分润予马姓，可保财路久不衰",
        "驿马星动宜远行，跨国事务得双赢\n机票改选航班号，内含6/8最显灵\n异国街头逢鼠辈，竟是关键引路人",
        "天解星临消宿业，法律纠纷终告捷\n重要文件备三份，印章勿离震位歇\n亥时有雨莫嫌烦，洗净前尘迎新契"
    ]},
    7: {"title": "鼎盛（巅峰级鸿运）", "texts": [
        "天乙贵人降凡尘，所求之事皆称心\n寅时祭祖得福荫，未刻提案获重金\n偶见双鱼跃门庭，速买彩券莫迟疑",
        "将星坐镇气势宏，竞技场上展峥嵘\n青绿战袍增运道，西方对手可先攻\n戌时若有犬吠急，捷报将至月明中",
        "帝旺当头运如虹，莫惧强敌敢争锋\n地产交易利午时，科技创新选申宫\n谨记分羹予兔姓，可避盛极反亏空"
    ]},
    8: {"title": "太和（终极祥瑞）", "texts": [
        "紫微高照天门开，鸾凤和鸣献瑞来\n三奇贵人齐相助，六合吉神共徘徊\n若求功名正当季，九天揽月非梦哉",
        "河图重现洛书显，天降甘露地涌泉\n跨国事务得利好，冷门投资翻倍赚\n红鸾星动正当时，良缘天成金玉伴",
        "青龙盘柱镇八方，文曲武曲同昭彰\n学术突破开新派，竞技超常破旧章\n亥子相交逢异梦，先祖指点迷津藏"
    ]}
}

# 指令处理
@yunshi_cmd.handle()
async def _(event: MessageEvent):
    global today_cache

    user_id = str(event.user_id)
    nickname = event.sender.nickname or f"用户{user_id[-4:]}"  # fallback 名字

    # 如果已有缓存直接返回
    if user_id in today_cache:
        data = today_cache[user_id]
    else:
        if random.random() < 0.7:
            # 模式1：0.7的概率，独立随机 a, b, c, d
            a = random.randint(0, 2)
            b = random.randint(0, 2)
            c = random.randint(0, 2)
            d = random.randint(0, 2)
            level = a + b + c + d
        else:
            # 模式2：0.3的概率，先随机生成 level，再分配 a, b, c, d
            level = random.randint(0, 8)
            while True:
                a = random.randint(0, 2)
                b = random.randint(0, 2)
                c = random.randint(0, 2)
                d = level - (a + b + c)
                if 0 <= d <= 2:
                    break
        level_info = YUNSHI_DATA[level]
        text = random.choice(level_info["texts"])
        stars = "★" * level + "☆" * (8 - level)

        data = {
            "level": level,
            "title": level_info["title"],
            "text": text,
            "stars": stars,
            "detail": f"财运({a})+姻缘({b})+事业({c})+人品({d})"
        }
        today_cache[user_id] = data
        save_cache(today_cache)

    # 输出构建
    msg = (
        f"@{nickname}，阁下的今日运势是：\n"
        f"{data['title']}\n"
        f"{data['stars']}\n"
        f"{data['text']}\n\n"
        f"{data['detail']}\n\n"
        f"仅供娱乐｜相信科学｜请勿迷信"
    )
    await yunshi_cmd.finish(msg)
