# Dockerfile
FROM python:3.11
ENV POETRY_VIRTUALENVS_CREATE=false
WORKDIR /secureblogs
# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION="1.3.1"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${POETRY_HOME}/venv/bin:${PATH}"
# Install system dependencies
COPY poetry.* pyproject.toml /secureblogs/
RUN poetry install
# Copy code and run web server
COPY . /secureblogs
EXPOSE 8000
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
CMD ["./docker-entrypoint.sh"]
