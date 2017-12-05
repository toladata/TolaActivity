FROM python:2.7

COPY . /code
WORKDIR /code

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install nginx -y

ADD docker/etc/nginx/nginx.conf /etc/nginx/nginx.conf

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "/code/docker-entrypoint.sh"]
