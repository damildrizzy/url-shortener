FROM python:3.8-alpine
LABEL maintainer="Samuel Adekoya"

ENV INSTALL_PATH /parsel
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "parsel.app:create_app()"