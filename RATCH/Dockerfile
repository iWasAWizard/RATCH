FROM python:3.8.5-buster

RUN apt update -y && \
    pip install --upgrade pip setuptools

COPY . /RATCH

RUN pip install -r /RATCH/requirements.txt

ENTRYPOINT [ "/bin/bash", "-c" ]

#CMD [ "python app.py" ]
CMD [ "flask run -h 0.0.0.0 -p 80" ]