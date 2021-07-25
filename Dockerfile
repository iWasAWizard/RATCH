FROM python:3.8.5

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt requirements-pgsql.txt config.py .env ./

RUN pip install -r requirements-pgsql.txt

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
