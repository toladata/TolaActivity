FROM python:2.7

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/code/docker-entrypoint.sh"]
