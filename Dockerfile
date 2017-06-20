FROM python:2.7

EXPOSE 8000

CMD ["sh", "-c", "pip install -r requirements.txt; python manage.py migrate; python manage.py loaddata fixtures/config/* ;python manage.py runserver 0.0.0.0:8000"]
