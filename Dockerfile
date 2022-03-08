FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y software-properties-common


RUN  add-apt-repository ppa:deadsnakes/ppa


RUN apt install python3.7


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]