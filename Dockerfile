# Builder stage
FROM python:3.12-slim AS builder
ARG GITHUB_USER
ARG GITHUB_TOKEN
RUN apt-get update && apt-get install -y git
RUN git config --global credential.helper store && echo "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install --only main
COPY . /app



FROM python:3.12-slim AS prod
RUN mkdir /app
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin -c "Docker image user" appuser
RUN chown -R appuser:appgroup app
USER appuser
RUN pip install poetry
RUN python -m poetry config virtualenvs.create false
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app
RUN python -m poetry install --only-root
CMD python -m poetry run start
