import hoshino, json
from hoshino import Service,priv
from nonebot import *
import requests, os
bot=get_bot()

sv1 = Service('退群通知', help_='退群通知')



@sv1.on_notice('group_decrease')
async def leave_notice(session: NoticeSession):
    type = session.event['sub_type']
    uid = session.event['user_id']
    gid = session.event['group_id']
    pid = session.event['operator_id']
    at = MessageSegment.at(pid)
    data = await bot.get_stranger_info(user_id= uid)
    name = data['nickname']
    if type == 'kick':
        await session.send(f"{at}认为{name}({uid})不适合本群")
    elif type == 'leave':
        await session.send(f"{name}({uid})离开了我们，相信会有再见的一天！")


sv2 = Service('入群欢迎', help_='入群欢迎')



FILE_FOLDER_PATH = os.path.dirname(__file__)
config_using = set()
CONFIG_PATH = os.path.join(FILE_FOLDER_PATH,'in_NoticeMessage.json')
class Config:
    def __init__(self, gid, config_path):
        self.gid = str(gid)
        self.config_path = config_path

    def __enter__(self):
        config_using.add(self.gid)
        return self

    def __exit__(self, type, value, trace):
        if self.gid in config_using:
            config_using.remove(self.gid)

    def load(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf8') as config_file:
                    return json.load(config_file)
            else:
                return {}
        except:
            return {}

    def save(self, config):
        try:
            with open(self.config_path, 'w', encoding='utf8') as config_file:
                json.dump(config, config_file, ensure_ascii=False, indent=4)
            return True
        except:
            return False

    def load_message(self):
        config = self.load()
        return config[self.gid] if self.gid in config else []

    def save_message(self, mes):
        config = self.load()
        config[self.gid] = mes
        return self.save(config)

@sv2.on_notice('group_increase')
async def increace_welcome(session: NoticeSession):
    
    if session.event.user_id == session.event.self_id:
        return  # ignore myself
    gid = session.event['group_id']
    uid = session.event['user_id']
    with Config(gid,CONFIG_PATH) as config:
        mes = config.load_message()
        await session.send(f'{mes}', at_sender=True)
# @sv2.on_fullmatch('test')
# async def test_mes(bot,ev):
#     gid = ev.group_id
#     with Config(gid,CONFIG_PATH) as config:
#         mes = config.load_message()
#         await bot.send(ev,f'ti{mes}')
@sv2.on_prefix('设置欢迎词')
async def set_message(bot, ev):
    message_temp = []
    gid = ev.group_id
    if not priv.check_priv(ev, priv.ADMIN):
        await bot.finish(ev, '只有群管理才能设置欢迎词', at_sender=True)
    with Config(gid, CONFIG_PATH) as config:
        for msg_seg in ev.message:
            if msg_seg.type == 'text' and msg_seg.data['text']:
                message_temp.append(msg_seg.data['text'].strip())
        if not message_temp:
            await bot.finish(ev, '你想设置的欢迎词要写在命令后面哦~',at_sender = True)
        else:
            message_temp = ''.join(message_temp)
            config.save_message(message_temp)
            await bot.finish(ev, '欢迎词设置成功。', at_sender = True)