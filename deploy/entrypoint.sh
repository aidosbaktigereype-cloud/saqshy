#!/bin/sh
# Перед запуском приложения применяем миграции и обновляем роли.
set -e
python manage.py migrate --noinput
python manage.py setup_roles
exec "$@"
