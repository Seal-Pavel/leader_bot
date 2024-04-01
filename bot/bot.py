from aiogram import Router, types
from aiogram.filters import CommandObject, Command

from utils.api_clients.base_api_client import BaseAPIClient

router = Router()

api_client = BaseAPIClient()


@router.message(Command(commands=["help"]))
async def help_command(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    await message.reply(
        disable_notification=True,
        text=f'ID этого чата: {chat_id}\n'
             f'Твой ID: {user_id}')


@router.message(Command(commands=["auth"]))
async def auth_command(message: types.Message, command: CommandObject):
    token = command.args

    if not token:
        await message.reply(
            disable_notification=True,
            text='Необходимы дополнительные аргументы.\n'
                 'Пример:\n'
                 '<code>/auth eyJ0eXAiOi...Lbs</code>\n'
                 'или\n'
                 '<code>/auth Bearer eyJ0eXAiOi...Lbs</code>')
        return

    if "eyJ0eXAiOi...Lbs" in token:
        await message.reply(
            disable_notification=True,
            text='Нет. Это просто пример')
        return

    url = "https://seal-pavel.website/leader/api/v1/token/update"
    data = {"token": token}
    await api_client.make_request(method="POST", endpoint=url, data=data)
