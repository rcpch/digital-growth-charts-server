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

# The bind-mounted workspace is owned by the host user, so git refuses to
# read it as a different uid ("dubious ownership") and provenance would
# report "unknown". Trust it explicitly for local dev/test runs.
RUN git config --global --add safe.directory /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]