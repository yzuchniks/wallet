Сделал, что успел.
Скажу честно работать с асинхронными задачами для меня было очень сложно, ранее мало сталкивался с этим.
Так и не смог по сути настроить. Но постарался сделать все что мог;)
Даже нормальную документацию не осталось времени написать, приношу извенения.

Для запуска проекта, находясь в директории */wallet/wallet_service/
выполнить команды:
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
