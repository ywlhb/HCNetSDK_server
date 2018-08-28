FROM tiangolo/uwsgi-nginx:python3.6-alpine3.7

WORKDIR /app

COPY . /app

COPY hcnetsdksvr.conf /etc/nginx/conf.d/
COPY ldconfig.conf /etc/ld.so.conf.d/

RUN apk update && apk add \
    libuuid \
    libstdc++ \
    && pip3 install --no-cache-dir -r requirements.txt

ENV LISTEN_PORT 8085

EXPOSE 8085 9085