FROM python:3.8.6-slim-buster as builder
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN pip install --disable-pip-version-check --no-cache-dir poetry && \
    poetry export --without-hashes -f requirements.txt > requirements.txt

FROM python:3.8.6-slim-buster
ARG USERNAME=python
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
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
RUN pip install --no-cache-dir .
USER ${USERNAME}:${USERNAME}
