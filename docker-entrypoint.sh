#!/bin/bash
echo "Iniciando o servidor..."
echo "OS: $(uname -a)"

# Se o SQL_LIBRARY estiver em branco ou for igual a sqlite, pula, se não instala
if [ -z "$SQL_LIBRARY" ] || [ "$SQL_LIBRARY" = "sqlite" ]; 
then 
    echo "Pulando a instalação da biblioteca $SQL_LIBRARY";
else 
    pip install $SQL_LIBRARY;
fi

# Coleta os arquivos estáticos
python manage.py collectstatic --noinput

# Cria migrações pendentes
python manage.py makemigrations

# Configuração das migrações
echo "Configurando o banco de dados..."
python manage.py makemigrations

# Aplicação das migrações
python manage.py migrate

# Realiza a população do banco de dados 
echo "Populando o banco de dados..."
python manage.py populate 100

# Inicia o servidor
python manage.py runserver 0.0.0.0:8000