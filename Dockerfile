FROM python:3.12-bookworm

# development or live
ARG BUILD_ENVIRONMENT="development"

ARG GITHUB_SHA
ENV GITHUB_SHA=${GITHUB_SHA}

COPY requirements/common-requirements.txt .

COPY requirements/${BUILD_ENVIRONMENT}-requirements.txt .

RUN pip install -r ${BUILD_ENVIRONMENT}-requirements.txt

EXPOSE 8000

WORKDIR /app

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]