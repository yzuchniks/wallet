Сделал, что успел.
Скажу честно работать с асинхронными задачами для меня было очень сложно, ранее мало сталкивался с этим.
Так и не смог по сути настроить. Но постарался сделать все что мог;)
Даже нормальную документацию не осталось времени написать, приношу извенения.

Для запуска проекта, находясь в директории */wallet/wallet_service/
создать файл .env с следующим содержимым:
```
POSTGRES_DB=ваше_имя_бд
POSTGRES_USER=ваш_пользователь_бд
POSTGRES_PASSWORD=ваш_пароль
DB_HOST=db
DB_PORT=5432

DJANGO_SETTINGS_MODULE=wallet_service.settings


CELERY_BROKER_URL=redis://redis:6379/0

REDIS_HOST=redis
REDIS_PORT=6379

DEBUG=True
SECRET_KEY=ваш_ключ
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

UID=1000
GID=1000
```

затем выполнить команды:
```
docker-compose build
docker-compose up
```

Для запуска тестов, в той же директории:
```
docker-compose run web pytest
```

Для запуска нагрузочного теста, войти в контейнер приложения:
```
docker exec -it django_app /bin/bash
```
Изнутри выполнить команду:
```
locust -f locustfile.py --host=http://localhost:8000 --users 1000 --spawn-rate 100 --run-time 1m
```
Перейти по адресу: http://localhost:8089

(Но они падают...)
