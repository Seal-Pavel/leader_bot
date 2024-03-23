import httpx

from datetime import datetime

from utils.usedesk_api_client import UsedeskAPIClient

from models.ticket import TicketData


class UsedeskService:
    def __init__(self, api_client: UsedeskAPIClient):
        self.api_client = api_client
        self.ticket: TicketData | None = None

    async def authenticate(self) -> None:
        await self.api_client.authenticate()

    async def load_ticket(self, ticket_data):
        self.ticket = ticket_data

    async def reply_to_reactivated_user(self, ticket_data, birthday):
        await self.load_ticket(ticket_data)

        is_mistake_in_age = (datetime.now().year - birthday.year) < 12
        if not is_mistake_in_age:
            text, files = self.get_minor_notification()
        else:
            text, files = self.get_incorrect_birth_year_notification()

        await self.send_message(ticket=self.ticket.id, message=text, fls=files)

    @staticmethod
    def get_minor_notification() -> tuple[str, list]:
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
    def get_incorrect_birth_year_notification() -> tuple[str, list]:
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

    async def send_message(self, ticket, message, fls: list[str] = None, agent_id=247423) -> httpx.Response:
        pass

    async def update_ticket(self, ticket, category_lid, field_id=19402, status=2) -> httpx.Response:
        pass
