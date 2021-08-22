FROM python:3.8.5

ENV FLASK_APP run.py

COPY run.py gunicorn-cfg.py requirements.txt requirements-postgres.txt config.py .env ./

RUN pip install -r requirements-postgres.txt

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
