FROM python:3.8.6-slim-buster as builder
WORKDIR /usr/src/app
ARG POETRY_VERSION=1.1.4
COPY pyproject.toml poetry.lock ./
RUN pip install --disable-pip-version-check --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.8.6-slim-buster
ARG PIP_VERSION=21.0.1
ARG USERNAME=python
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==${PIP_VERSION} && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt \
    /bin/umount \
    /usr/bin/chfn \
    /usr/bin/newgrp \
    /bin/su \
    /usr/bin/passwd \
    /usr/bin/expiry \
    /usr/bin/chsh \
    /usr/bin/wall \
    /usr/bin/gpasswd \
    /bin/mount \
    /sbin/unix_chkpwd \
    /usr/bin/chage && \
    groupadd -r ${USERNAME} && \
    useradd --no-log-init -r -g ${USERNAME} ${USERNAME}
COPY . .
USER ${USERNAME}:${USERNAME}
