# Social network analog

Corporate microblogging service similar to Twitter.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![ElasticSearch](https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch)![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?style=for-the-badge&logo=grafana&logoColor=white)![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)
![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

## Features
- async FastAPI & SQLAlchemy
- Prometheus datasource & dashboard loaded in Grafana automatically
- Sentry introduced
- EFK stack introduced
- Pytest coverage (in developing)
- Linting by ... (in developing)

## Tech

- [Python 3.10](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Docker](https://www.docker.com/)
- [Poetry](https://pypi.org/project/poetry/)
- [pytest](https://pypi.org/project/pytest/)
- [aiofiles](https://pypi.org/project/aiofiles/)
- [pgAdmin](https://www.pgadmin.org/)
- [Sentry](https://pypi.org/project/sentry-sdk/)
- [Prometheus_fastapi_instrumentator](https://pypi.org/project/prometheus-fastapi-instrumentator/)
- [Grafana](https://grafana.com/)
- [Fluentd](https://www.fluentd.org/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Kibana](https://www.elastic.co/kibana/)

## Pre-Installation (not required)

1. Preparing to launch Sentry:
- create an account
- create a new project with selected `FASTAPI` platform
- get and save individual `DSN` key for `.env` file
Docs: https://docs.sentry.io/platforms/python/

2. Quick start for Kibana: [Guide](https://www.elastic.co/guide/en/kibana/current/get-started.html#_required_privileges)
**Data source already added**, just create an account and discover

## Installation

- Create project folder
- Clone rep: 
    ```
    git clone ...
    ```

- Complete the `.env` file with environment variables:
    ```
    POSTGRES_SERVER=db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_DB=app
    
    PGADMIN_DEFAULT_EMAIL = test@mail.ru
    PGADMIN_DEFAULT_PASSWORD = password
    PGADMIN_LISTEN_ADDRESS = [0.0.0.0.]
    PGADMIN_LISTEN_PORT=8080
    
    OUT_FILE_PATH = /srv
    
    SENTRY_DSN = https://examplePublicKey@o0.ingest.sentry.io/0
    ```

**OPTIONAL**
- Use the package manager [poetry](https://pypi.org/project/poetry/) to install foobar:

- with dev packages:
    ```bash
    cd PROJECT_PATH && poetry install
    ```
- without dev packages:
    ```bash
    cd PROJECT_PATH && poetry install --only main
    ```

## Usage

Project build
```
docker-compose up --build -d
```

## Дополнительная информация
- Sentry доступен по адресу ...
- Grafana автоматически подгружает datasource и dashboard со сборкой проекта, которые уже доступны по адресу
- Kibana доступна по адресу... источник будет подгружен в течении 5-7 минут

## Available local resources
- [Interactive API docs (Swagger UI)](http://localhost:80/docs)
- [pgAdmin](http://localhost:8080/)
- [Sentry](http://localhost:8080/)
- [Grafana](http://localhost:3000)
- [Kibana](http://localhost:5601)
