FROM python:3.8

LABEL maintainer="polonity <hiken.pc@gmail.com>"

RUN pip install flask
RUN pip install web3

ADD . /code
WORKDIR /code

CMD ["python3", "app.py"]