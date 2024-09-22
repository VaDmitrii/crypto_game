FROM python:3.11-slim

WORKDIR app/

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/ .

ENV PYTHONPATH="/app"

CMD ["python", "telegram_bot/bot.py"]
