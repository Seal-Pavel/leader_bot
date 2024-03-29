FROM python:3.10-slim

WORKDIR /leader-bot

ENV PYTHONPATH /leader-bot
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

RUN chmod +x app/entrypoint.sh

CMD ["app/entrypoint.sh"]