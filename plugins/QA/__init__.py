import nonebot
from nonebot.adapters.kaiheila import Adapter as KaiheilaAdapter

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(KaiheilaAdapter)

SU = on_command(
    "su",
    aliases = {"superuser"},
    rule = to_me(),
    permission = SUPERUSER,
    priority = 10,
    block = True
    )

@SU.handle()
async def _():
    await SU.finish("as root")

GF = on_command(
    "gf",
    aliases = {"get_girlfriend"},
    rule = to_me(),
    priority = 10,
    block = True
    )

@SU.handle()
async def _():
    if isinstance(event,message.group.kmarkdown):
        await SU.finish("as root")
    else:
        return ""
    

@GF.handle()
async def _():
    if isinstance(Event,kmarkdown):
        await GF.finish("呼噜噜")
    else:
        await GF.finish("ERR")
    