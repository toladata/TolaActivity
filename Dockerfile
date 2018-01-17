FROM python:2.7

COPY . /code
WORKDIR /code

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install nginx -y

ADD docker/etc/nginx/tola.conf /etc/nginx/conf.d/tola.conf

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["/code/docker-entrypoint.sh"]
