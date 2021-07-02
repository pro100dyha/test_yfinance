FROM python:3.8.6

WORKDIR /opt/www/app

RUN pip install --upgrade pip

ADD . /opt/www/app

RUN pip install -r requirements.txt

EXPOSE 5000

