FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE purrfect_care.settings

WORKDIR /webapp-backend

COPY . /webapp-backend

RUN pip install --no-cache-dir -r requirements.txt