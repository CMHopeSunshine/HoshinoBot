from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
====================
= HoshinoBot使用说明 =
====================
发送[]内的关键词触发
本帮助文档为HoshinoBot的帮助
Adachi-BOT的请输入[#help]
[#帮助 原神/工具/娱乐](查看各功能详细帮助)
====== 常用指令 ======
[#原神日历]查看原神活动日历
[#原神估价 uid]查看账号估值
[#原神猜语音]顾名思义猜语音
[#点歌 歌曲名]搜歌点歌
[#表白 对象]发一篇表白小作文
[#续写 内容]ai续写文章
[#生成表情包 文字]生成表情包
[#要我一直 图片]生成表情包
[#塔罗牌]塔罗牌占卜
[#rua@xxx]rua一下其他头像
[#remake]人生重来模拟器
[#青年大学习]查看最新期答案
[#来n张(关键词)色/涩/瑟图]懂
[#code 语言 (-i) (输入) 代码]在线运行代码
[#搜天气 城市名]看城市天气
[#翻译中|英|日 内容]翻译
[#rss addb up主号]订阅b站up主信息
=====================
'''.strip()
#[#喜加一资讯 n]查看n条喜加一资讯

def gen_service_manual(service: Service, gid: int):
    spit_line = '=' * max(0, 18 - len(service.name))
    manual = [f"|{'○' if service.check_enabled(gid) else '×'}| {service.name} {spit_line}"]
    if service.help:
        manual.append(service.help)
    return '\n'.join(manual)


def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for s in service_list:
        if s.visible:
            manual.append(gen_service_manual(s, gid))
    return '\n'.join(manual)


@sv.on_prefix('#帮助')
async def send_help(bot, ev: CQEvent):
    gid = ev.group_id
    arg = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    services = Service.get_loaded_services()
    if not arg:
        await bot.send(ev, TOP_MANUAL)
    elif arg in bundles:
        msg = gen_bundle_manual(arg, bundles[arg], gid)
        await bot.send(ev, msg)
    elif arg in services:
        s = services[arg]
        msg = gen_service_manual(s, gid)
        await bot.send(ev, msg)
    # else: ignore
