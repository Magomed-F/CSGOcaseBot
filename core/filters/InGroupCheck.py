from aiogram import Bot
from aiogram.types import Message, Update,CallbackQuery
from aiogram.filters import BaseFilter

list_of_channels = [-1002157786722]

async def InGroupCheck(user_id, bot: Bot) -> bool:
    num = 0
    for channel in list_of_channels:
        member = await bot.get_chat_member(channel, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            num += 1
        else:
            pass
    if num == len(list_of_channels):
        return True
    else:
        return False
