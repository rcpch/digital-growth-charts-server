FROM python:3.8-buster

RUN apt-get update -y

ENV FLASK_ENV=development
ENV FLASK_APP=app.py

WORKDIR /app

COPY . /app

EXPOSE 5000

RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "5000"]