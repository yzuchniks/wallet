# Используем официальный минимальный образ Python
FROM python:3.11-slim

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (нужны для работы PostgreSQL и компиляции пакетов)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Указываем команду по умолчанию для запуска контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
