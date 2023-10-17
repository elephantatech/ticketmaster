# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install poetry
RUN pip install -U pip setuptools wheel
RUN pip install pdm


# Set the working directory in docker
WORKDIR /src

# Copy poetry lock and pyproject.toml file
COPY pyproject.toml readme.md LICENSE /src/
# Copy the content of the local src directory to the working directory
COPY ./app /src/app/

# Install dependencies
RUN pdm install --prod --no-lock --no-self --no-editable
EXPOSE 8000
# Specify the command to run on container start
CMD ["pdm","run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
