FROM python:3.8

LABEL maintainer="polonity <hiken.pc@gmail.com>"

RUN pip install flask
RUN pip install substrate-interface

ADD . /code
WORKDIR /code

CMD ["python3", "app.py"]