FROM python:3.12-bookworm

COPY requirements/common-requirements.txt .

COPY requirements/development-requirements.txt .

RUN pip install -r development-requirements.txt

EXPOSE 8000

WORKDIR /app

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]