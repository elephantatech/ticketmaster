# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.6.1

# Set the working directory in docker
WORKDIR /app

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry lock and pyproject.toml file
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the content of the local src directory to the working directory
COPY ./app /app/

# Specify the command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
