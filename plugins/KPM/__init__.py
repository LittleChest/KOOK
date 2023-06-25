from nonebot.adapters.kaiheila import Event, Bot
from nonebot import get_driver, on_message, on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER

driver = get_driver()

switch = True

switch_ON = on_command(
    "打开互通",
    aliases = {"开启互通"},
    rule = to_me(),
    permission = SUPERUSER,
    priority = 10,
    block = True
    )

@switch_ON.handle()
async def _():
    global switch
    switch = True
    await switch_ON.finish("已开启与Minecraft服务器的连接")

switch_OFF = on_command(
    "关闭互通",
    aliases = {"停止互通"},
    rule = to_me(),
    permission = SUPERUSER,
    priority = 10,
    block = True
    )

@switch_OFF.handle()
async def _():
    await switch_OFF.finish("已临时屏蔽与Minecraft服务器的连接")

"""
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN,GROUP_OWNER
"""

from nonebot.log import logger
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pathlib import Path
from .utils import (
    channel_list,
    mc_log_path,
    mcrcon_password,
    mcrcon_port
    )
from .utils import mcrcon_connect, mc_translate, log_to_dict

log = Path(mc_log_path) / "latest.log"
if log.exists():
    logger.success(f"已找到 {log}")
    driver = get_driver()
    @driver.on_bot_connect
    async def _(bot: Bot):
        global switch
        with open(log, "r", encoding = "utf8") as fp:
            pos = fp.seek(0,2)
        while True:
            if switch == False:
                await asyncio.sleep(1)
                continue
            else:
                fp = open(log, "r", encoding = "utf8")
                fp.seek(pos, 0)
                if line := fp.read():
                    pos = fp.seek(0,2)
                    line.replace("\r\n","\n")
                    line = line.strip('\n').split('\n')
                    for x in line:
                        if msg_dict := log_to_dict(x):
                            msg = f'【{msg_dict["nickname"]}】{msg_dict["message"]}'
                            for channel in channel_list:
                                await bot.send_channel_msg(channel_id = channel['channel_id'],message = msg)
                fp.close()
                await asyncio.sleep(1)
else:
    logger.error(f"mc_log_path 地址设置错误，{log} 不存在。")

# 定义CUSTOMER权限

async def CUSTOMER(event: Event) -> bool:
    for channel in channel_list:
        if event.channel_id == channel["channel_id"]:
            return True
    else:
        return False

flag = True

mcr = asyncio.run(mcrcon_connect("127.0.0.1", mcrcon_password, mcrcon_port))
async def check():
    return switch and (mcr or flag)

send = on_message(rule = check, permission = CUSTOMER, priority = 10)
@send.handle()
async def _(bot: Bot, event: Event):
    global flag, mcr
    msg = await mc_translate(bot, event)
    try:
        mcr.command(msg)
        flag = True
    except:
        flag = False
        mcr = None
        mcr = await mcrcon_connect("127.0.0.1", mcrcon_password, mcrcon_port)