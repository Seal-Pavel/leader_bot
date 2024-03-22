from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["help"]))
async def help_command(message: types.Message):
    await message.answer('Leader-ID', disable_notification=True)


@router.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)
