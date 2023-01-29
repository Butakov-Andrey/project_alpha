# Project Alpha
Проект реализован в виде монорепозитория для микросервисов backend и frontend  

Установить pre-commit хуки:
```
$ pre-commit install
```
[Указать директорию](.pre-commit-config.yaml) с приложением в которой будут отрабатывать pre-commit хуки:  
```
files: ^backend/web/
```
Создание образов и запуск контейнеров:
```
$ docker-compose up -d --build
```

# *server*
## Nginx
pass

# *backend*
## Web
Создать директорию *backend/web/alembic/versions/*  
Cоздать миграции:
```
$ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Проверить сгенерированные миграции в директории *backend/web/alembic/versions/*  
Применить миграции и обновить базу данных:
```
$ docker-compose exec web alembic upgrade head
```
Создать директорию *backend/web/logs/*, куда будут сохраняться логи  

# *frontend*
pass