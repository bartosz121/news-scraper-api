FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

COPY . /usr/src/app/

WORKDIR /usr/src/app/news_scraper_api

CMD ["gunicorn", "--conf", "gunicorn_config.py", "--bind", "0.0.0.0:5000", "app:create_app()"]
