#!/usr/bin/env bash
# O comando abaixo garante que o script falhe imediatamente se qualquer comando falhar (Fail-Fast)
set -o errexit

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos (WhiteNoise)..."
python manage.py collectstatic --no-input

echo "Aplicando migrações no banco de dados Neon..."
python manage.py migrate