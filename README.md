# Fastapi template
Для запуска приложения в корень проекта необходимо добавить файл с переменными окружения .env  
При разработке в Docker в файле .env указать имя контейнера с БД (db)  

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
$ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Проверить сгенерированные миграции в папке versions/.  
Применить миграции и обновить базу данных:
```
$ docker-compose exec web alembic upgrade head
```

## Логирование
Логи сохраняются в директорию /logs  
Новый файл создается каждую неделю