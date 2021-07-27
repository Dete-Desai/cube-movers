#!/bin/sh

while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

echo "Database now is available on internal 3306 port"
python ./server/manage.py makemigrations && python ./server/manage.py migrate &&\
python ./server/manage.py runserver 0.0.0.0:8000