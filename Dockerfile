FROM python:3.8.6-slim-buster as builder
WORKDIR /usr/src/app
ARG POETRY_VERSION=1.1.5
COPY pyproject.toml poetry.lock ./
RUN pip install --disable-pip-version-check --no-cache-dir poetry==${POETRY_VERSION} && \
    poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.8.6-slim-buster
ARG PIP_VERSION=21.0.1
ARG USERNAME=python
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends\
        apt=1.8.2.2 \
        libapt-pkg5.0=1.8.2.2 \
        libp11-kit0=0.23.15-2+deb10u1 \
        libsqlite3-0=3.27.2-3+deb10u1 \
        libssl1.1=1.1.1d-0+deb10u6 \
        libzstd1=1.3.8+dfsg-3+deb10u2 \
        openssl=1.1.1d-0+deb10u6 && \
    pip install --no-cache-dir --upgrade pip==${PIP_VERSION} && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf \
        requirements.txt \
        /bin/mount \
        /bin/umount \
        /bin/su \
        /usr/bin/chage \
        /usr/bin/chfn \
        /usr/bin/chsh \
        /usr/bin/expiry \
        /usr/bin/gpasswd \
        /usr/bin/newgrp \
        /usr/bin/passwd \
        /usr/bin/wall \
        /sbin/unix_chkpwd \
        /var/lib/apt/lists/* && \
    groupadd -r ${USERNAME} && \
    useradd --no-log-init -r -g ${USERNAME} ${USERNAME}
COPY . .
USER ${USERNAME}:${USERNAME}
