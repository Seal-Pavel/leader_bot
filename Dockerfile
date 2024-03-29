FROM python:3.10-slim

WORKDIR /leader_bot

ENV PYTHONPATH /leader_bot
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]