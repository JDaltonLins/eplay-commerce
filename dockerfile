#!/bin/bash

# Copia do diretorio local para o container
FROM python:3.12-rc

# Define as variaveis de ambiente
ENV APP_HOME=/container/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualiza o sistema operacional
RUN apt update && apt upgrade --yes

# Altera a pasta de acesso
WORKDIR $APP_HOME

# Atualiza o pip
RUN pip install --upgrade pip

# Copia os arquivos para o container
COPY . $APP_HOME

# Instalação de dependências
RUN pip install -r requirements.txt


COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["bash", "docker-entrypoint.sh"]

EXPOSE 8000
STOPSIGNAL SIGTERM