from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["help"]))
async def help_command(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.answer('Тебе никто не поможет.', disable_notification=True)
    await message.reply(f'ID этого чата: {chat_id}\nТвой ID: {user_id}', disable_notification=True)
