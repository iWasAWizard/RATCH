FROM python:3.8.5

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt requirements-pgsql.txt config.py .env ./
#COPY app app

RUN pip install -r requirements-pgsql.txt

EXPOSE 5000

CMD ["gunicorn", "--reload", "--config", "gunicorn-cfg.py", "run:app"]
