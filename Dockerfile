FROM python:3.8.6-slim-buster as builder
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN pip install --disable-pip-version-check --no-cache-dir poetry && \
    poetry export --without-hashes -f requirements.txt > requirements.txt

FROM python:3.8.6-slim-buster
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY reversi reversi