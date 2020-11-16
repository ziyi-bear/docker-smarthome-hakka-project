FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install requests

COPY ./客語文字轉語音.py /app/main.py
COPY ./uwsgi.ini /app/uwsgi.ini