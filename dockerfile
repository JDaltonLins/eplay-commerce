#!/bin/bash

# Irá realizar a clonagem e configuração do repositório do projeto django junto a configuração do serviço de 
# e-mail (docker-mailserver)

# Copia do diretorio local para o container
FROM python:3.12-rc-alpine3.17

COPY . /

# Atualiza o sistema operacional
RUN apk update

# Atualiza o pip
RUN pip install --upgrade pip

# Instala as dependencias do pillow
RUN apk add build-base tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev

# Instalação de dependências
RUN pip install -r requirements.txt

# Configuração das migrações
RUN python manage.py makemigrations

# Aplicação das migrações
RUN python manage.py migrate
