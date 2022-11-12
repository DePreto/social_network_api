FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /src

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY . /src

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV PYTHONPATH=/src:/src/app

CMD poetry run alembic upgrade head && uvicorn --host 0.0.0.0 --port 80 app.main:app
