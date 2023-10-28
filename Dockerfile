FROM python:3.8-buster

RUN apt-get update -y

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--reload"]