FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

WORKDIR /app

COPY ./requirement.txt /app/requirement.txt

RUN pip install -r requirement.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
