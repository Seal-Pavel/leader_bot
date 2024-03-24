import os
import httpx
import aiofiles

from datetime import datetime, time

from models.ticket import TicketData

from utils.api_clients.usedesk_api_client import UsedeskAPIClient
from utils.logger import get_logger

logger = get_logger(__name__)

CONSENT_PERSONAL_DATA_PATH = "../statics/files/Согласие на обработку персональных данных.docx"
CONSENT_DISTRIBUTION_PERSONAL_DATA_PATH = "../statics/files/Согласие на распространение персональных данных.docx"

USEDESK_PAVEL_ID = int(os.getenv("USEDESK_PAVEL_ID"))
USEDESK_DENIS_ID = int(os.getenv("USEDESK_DENIS_ID"))
USEDESK_NIKA_ID = int(os.getenv("USEDESK_NIKA_ID"))


class UsedeskService:
    def __init__(self, api_client: UsedeskAPIClient):
        self.api_client = api_client
        self.ticket: TicketData | None = None

    async def authenticate(self, token) -> None:
        await self.api_client.authenticate(token)

    async def load_ticket(self, ticket_data):
        self.ticket = ticket_data

    async def reply_to_reactivated_user(self, ticket_data, birthday) -> None:
        await self.load_ticket(ticket_data)

        is_mistake_in_age = (datetime.now().year - birthday.year) < 12
        if not is_mistake_in_age:
            text, files = self.get_minor_notification()
        else:
            text, files = self.get_incorrect_birth_year_notification()

        await self.send_message(message=text, ticket_id=self.ticket.id, files=files)
        await self.update_ticket(ticket_id=self.ticket.id, category_lid="Редактирование профиля")

        logger.info(f"The user with email {self.ticket.client_email} will receive a response ({self.ticket.id=}).")

    async def get_minor_notification(self) -> tuple[str, list[tuple[str, bytes] | None]]:
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

        files = await self.prepare_files([CONSENT_PERSONAL_DATA_PATH, CONSENT_DISTRIBUTION_PERSONAL_DATA_PATH])
        return text, files

    async def get_incorrect_birth_year_notification(self) -> tuple[str, list[tuple[str, bytes] | None]]:
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

        files = await self.prepare_files([])
        return text, files

    @staticmethod
    async def prepare_files(file_paths: list = None) -> list[tuple[str, bytes] | None]:
        files = []
        for file_path in file_paths:
            async with aiofiles.open(file_path, 'rb') as f:
                files.append((file_path, await f.read()))
        return files

    @staticmethod
    async def get_current_agent_id() -> int | None:
        now = datetime.now()
        weekday = now.weekday()
        current_time = now.time()

        # Pavel works on Saturday (5) and Sunday (6) from 09:00 to 23:00
        if weekday in [5, 6] and time(9, 0) <= current_time <= time(23, 0):
            return USEDESK_PAVEL_ID

        # Denis works on weekdays from 18:00 to 23:00
        if weekday in range(0, 5) and time(18, 0) <= current_time <= time(23, 0):
            return USEDESK_DENIS_ID

        # Nika works on weekdays from 10:00 to 18:00
        if weekday in range(0, 5) and time(10, 0) <= current_time <= time(18, 0):
            return USEDESK_NIKA_ID

    async def send_message(self, message, ticket_id, files=None) -> httpx.Response:
        agent_id = await self.get_current_agent_id()
        return await self.api_client.send_message(message=message, ticket_id=ticket_id, files=files, agent_id=agent_id)

    async def update_ticket(self, ticket_id, category_lid) -> httpx.Response:
        return await self.api_client.update_ticket(ticket_id, category_lid)
