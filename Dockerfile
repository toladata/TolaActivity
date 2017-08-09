FROM python:2.7

COPY . /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate; python manage.py runserver 0.0.0.0:8000"]
