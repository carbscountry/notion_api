FROM python:3.9-buster

ARG work_dir="/workspace"
#kaggle apiをコンテナに格納
RUN apt-get update \
    && apt-get install -y \
    vim \
    wget \
    curl \
    git

# Poetry インストール
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  PYSETUP_PATH="/opt/pysetup"
# Nodejs の導入
RUN curl -sL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs

RUN pip install poetry
