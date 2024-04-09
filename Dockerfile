# Dockerfile to build image for both FastAPI server and MkDocs documentation containers
FROM python:3.12-bookworm

# Extra packages required for Material for MkDocs plugins (dependency for git and pdf plugins)
RUN apt-get update \
    && apt install -y git python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0

# Add FastAPI Server requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add MkDocs requirements
COPY documentation/docs-requirements.txt .
RUN pip install -r docs-requirements.txt

EXPOSE 8000

# Set current working directory to /app
WORKDIR /app

# Copy codebase into /app
COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]