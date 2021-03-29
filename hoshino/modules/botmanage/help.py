from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
=====================
- HoshinoBot使用说明 -
------神州限定版------
=====================
发送方括号[]内的关键词即可触发
※功能采取模块化管理，群管理可控制开关

[rua@群成员] rua头像
[ys#uid] 原神信息查询
[@bot相遇之缘] 卡池十连模拟
[***哪里有] 原神资源位置
[点歌+歌名] 网易云音乐点歌
[丘丘一下] 丘丘语翻译
[lssv] 查看功能模块的开关状态（群管理限定）
[来杯咖啡] 出问题了，联系无量塔

发送以下关键词查看更多：
[来张色图]
[到点了]
[原神公告]
[.r]
========
※除这里中写明外 另有其他隐藏功能:)
※隐藏功能属于赠品 不保证可用性
※本bot开源，可自行搭建
※您的支持是本bot更新维护的动力
※※调教时请注意使用频率，您的滥用可能会导致bot账号被封禁
'''.strip()

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix(('help', '帮助'))
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        await bot.send(ev, msg)
    # else: ignore
