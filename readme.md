# Ticketmaster API

A simple ticket management API built with FastAPI.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [Running the Tests](#tests)
- [Test Results](md_report.md)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)]

## Getting Started

### Prerequisites

- Python 3.x
- Redis 6.2
- poetry
- docker
- docker compose

### Installing

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/ticketmaster.git
    ```

2. Install dependencies using Poetry

    ```bash
    cd ticketmaster
    poetry install
    ```

## Tests

Run tests using pytest:

```bash
poetry run pytest --cov=./app --cov-report=term --cov-fail-under=70 -vvv tests
```

## Usage

Running the Project with Docker Compose
Prerequisites:

- Docker
- docker-compose

1. Build and run the application.
    This command will start the FastAPI server and any other services defined in your docker-compose.yml:

    ```bash
    docker-compose up --build
    ```

    detached mode

    ```bash
    docker-compose up --build -d
    ```

2. Accessing the application
    Open a web browser and navigate to:

    ```bash
    http://localhost:8000
    ```

3. Stopping the application

    To stop the services, simply press CTRL+C in the terminal where docker-compose up is running.

    Alternatively, you can run:

    ```bash
    docker-compose down

    ```

Notes:
The Docker Compose setup is suitable for development purposes. For deploying in production, you may need additional configurations and optimizations.

If you modify the code or add new dependencies, you might need to rebuild the Docker image. You can do this using the docker-compose up --build command.

## Contributing

1. Fork the project.
2. Create a new branch for your feature (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -am 'Add some feature').
4. Push the branch (git push origin feature/YourFeature).
5. Open a pull request.

## License

TBD opensource license
