import os

from urllib.parse import urljoin

from typing import Tuple

from utils.usedesk_api_client import UsedeskAPIClient

from dotenv import load_dotenv

load_dotenv()

_USEDESK_API_HOST = os.getenv("USEDESK_API_HOST")
USEDESK_API_CREATE_MSG = urljoin(_USEDESK_API_HOST, "create/comment")
USEDESK_API_UPDATE_TICKET = urljoin(_USEDESK_API_HOST, "update/ticket")
USEDESK_API_GET_FIELDS = urljoin(_USEDESK_API_HOST, "ticket/fields")

USEDESK_API_TOKEN = os.getenv('USEDESK_API_TOKEN')


class UsedeskService:
    def __init__(self, api_client: UsedeskAPIClient):
        self.api_client = api_client

    async def authenticate(self) -> None:
        await self.api_client.authenticate()

    @staticmethod
    def get_minor_notification() -> Tuple[str, list]:
        text = """
            <p>Здравствуйте!</p>
            <p>Ваш профиль был деактивирован по причине того, что вы не загрузили сканы согласий родителей на обработку ваших персональных данных в свой профиль.<br/>
            Временно активировали ваш профиль и продлили срок для загрузки согласий на 30 дней.<br/>
            Пожалуйста, загрузите сканы согласий в разделе — <a href="https://leader-id.ru/settings?tab=privacy">https://leader-id.ru/settings?tab=privacy</a>, иначе ваш профиль будет вновь деактивирован.</p>
            <p>Подробности можно прочитать в статье:<br/>
            <a href="http://leader-id.usedocs.com/article/42745">Где заполнить согласие несовершеннолетнего на обработку персональных данных?</a></p>
            <p>Если у вас остались вопросы, мы с радостью на них ответим.<br/>
            Служба поддержки Leader-ID.<br/>
            <a href="mailto:support@leader-id.ru">support@leader-id.ru</a></p>
            <hr/>
            <p>Основные вопросы и ответы в разделе «<a href="http://leader-id.usedocs.com/">Частые вопросы</a>»</p>
            <hr/>
            <p>Вы можете написать в наш чат-бот <a href="https://t.me/leaderid_bot" target="_blank">Telegram</a></p>
        """.strip()
        files = ["statics/files/Согласие на обработку персональных данных.docx",
                 "statics/files/Согласие на распространение персональных данных.docx"]
        return text, files

    @staticmethod
    def get_incorrect_birth_year_notification() -> Tuple[str, list]:
        text = """
            <p>Здравствуйте!</p>
            <p>Ваш профиль был деактивирован, так как в настройках указан некорректный год рождения.<br/>
            Мы активировали профиль, пожалуйста, измените дату рождения, перейдя по ссылке: <a href="https://leader-id.ru/settings?tab=main">https://leader-id.ru/settings?tab=main</a>.</p>
            <br/>
            <p>Просим вас пройти небольшой <a href="https://pnp.leader-id.ru/polls/p/67645e46-f179-45f1-8caf-50ec0bcd99c8/" target="_blank">опрос удовлетворенности поддержкой</a>. Это позволит нам улучшить ее качество.</p>
            <br/>
            <p>Если у вас остались вопросы, мы с радостью на них ответим.<br/>
            Служба поддержки Leader-ID.<br/>
            <a href="mailto:support@leader-id.ru">support@leader-id.ru</a></p>
            <hr/>
            <p>Основные вопросы и ответы в разделе «<a href="http://leader-id.usedocs.com/">Частые вопросы</a>»</p>
            <hr/>
            <p>Вы можете написать в наш чат-бот <a href="https://t.me/leaderid_bot" target="_blank">Telegram</a></p>
        """.strip()
        files = []
        return text, files
