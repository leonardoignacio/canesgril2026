#!/usr/bin/env bash
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos (WhiteNoise)..."
python manage.py collectstatic --no-input

echo "Aplicando migrações no banco de dados Neon..."
python manage.py migrate

# Comandos no Render
#Build Command: ./build.sh
#Start Command: gunicorn canesgril.wsgi:application