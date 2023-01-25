# Fastapi template
Шаблон реализован в виде монорепозитория для микросервисов (web в директории web/)  
Для запуска приложений в корень проекта необходимо добавить файл с переменными окружения .env  
При разработке в Docker в файле .env указать имя контейнера с БД (db)  

## Для разработки в Docker:
Создание образов и запуск контейнеров:
```
$ docker-compose up -d --build
```

## Pre-commit
Установить pre-commit хуки:
```
$ pre-commit install
```
[Указать директорию](.pre-commit-config.yaml) с приложением в которой будут отрабатывать pre-commit хуки:  
```
files: ^web/
```

## Миграции для приложения web
Создать директорию web/alembic/versions/  
Cоздать миграции:
```
$ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Проверить сгенерированные миграции в директории web/alembic/versions/  
Применить миграции и обновить базу данных:
```
$ docker-compose exec web alembic upgrade head
```

## Логирование
Создать директорию web/alembic/versions/  
Логи сохраняются в директорию web/logs/  