# Fastapi template
Для запуска приложения в корень проекта необходимо добавить файл с переменными окружения .env  
При локальной разработке в файле .env указать ip и порт контейнера с БД (localhost:5432)  
При разработке в Docker в файле .env указать имя контейнера с БД (db)  


## Для локальной разработки:
### База данных Postgres в контейнере Docker
Создание docker network:
```
$ docker network create test-net
```
Создание хранилища:
```
$ docker volume create --name postgres_data
```
Создание образа:
```
$ docker build -t test-db -f docker/db.Dockerfile .
```
Создание и запуск контейнера:
```
$ docker run -d \
    --name test-db \
    --env-file ./.env \
    --network=test-net \
    -v postgres_data:/var/lib/postgresql/data/ \
    -p 5432:5432 \
    test-db
```

### Web-приложение
Запуск приложения локально:
```
$ uvicorn core.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
```

## Для разработки в Docker:
Создание образов и запуск контейнеров web и db:
```
$ docker-compose up -d --build
```

## Pre-commit
Установить pre-commit хуки:
```
$ pre-commit install
```

## Миграции
В папке alembic/ создать миграцию:
```
$ alembic revision --autogenerate -m "Testing table"
(Docker) $ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Проверить сгенерированные миграции в папке versions/.  
Применить миграции и обновить базу данных:
```
$ alembic upgrade head
(Docker) $ docker-compose exec web alembic upgrade head
```

## Логирование
Логи сохраняются в директорию /logs  
Новый файл создается каждую неделю