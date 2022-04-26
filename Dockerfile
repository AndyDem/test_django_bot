FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TG_BOT_TOKEN=YOUR_TG_BOT_TOKEN
WORKDIR /usr/src/app
RUN pip install --upgrade pip
COPY . /usr/src/app
RUN pip install -r ./requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate