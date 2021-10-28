FROM python:3.8-slim-buster

RUN pip install numpy dash pandas

WORKDIR /app
COPY . /app

CMD [ "python3", "main.py" ]