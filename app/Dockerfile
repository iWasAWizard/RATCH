FROM python:3.9.5-buster

RUN apt update -y && \
    pip install --upgrade pip setuptools

COPY . /app

WORKDIR /app

RUN pip install -r /app/requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
