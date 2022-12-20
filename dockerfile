#!/bin/bash

# Irá realizar a clonagem e configuração do repositório do projeto django junto a configuração do serviço de 
# e-mail (docker-mailserver)

# Copia do diretorio local para o container
FROM python:3.12-rc-alpine3.17

COPY . /container/

# Atualiza o sistema operacional
RUN apk update && apk upgrade

# Atualiza o pip
RUN pip install --upgrade pip

# Instala as dependencias do pillow
RUN apk add build-base tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

# Altera a pasta de acesso
WORKDIR /container/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalação de dependências
RUN pip install -r requirements.txt

# Configuração das migrações
RUN python manage.py makemigrations

# Aplicação das migrações
RUN python manage.py migrate

# Realiza a população do banco de dados
RUN python manage.py populate 100

EXPOSE 8000
STOPSIGNAL SIGTERM