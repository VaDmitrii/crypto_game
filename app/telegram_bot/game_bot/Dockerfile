# telegram/game_bot/Dockerfile
FROM python:3.11-slim

WORKDIR app/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PYTHONPATH="/app"

COPY ./app/ .

CMD ["python", "telegram_bot/game_bot/game_bot.py"]
