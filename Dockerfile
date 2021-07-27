FROM  python:2-alpine3.9


RUN apk update\
  && apk add --virtual build-deps gcc musl-dev \
  && apk add --no-cache mariadb-connector-c-dev\
  && apk add build-base\
  && pip install mysqlclient\
  && apk add jpeg-dev zlib-dev libjpeg\
  && apk add mariadb-plugin-rocksdb\ 
  && apk del build-deps


RUN apk add netcat-openbsd


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysql-connector-python

COPY . ./

EXPOSE 8000

