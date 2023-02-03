# Project Alpha
Проект реализован в виде монорепозитория  

Установить pre-commit хуки:
```
$ pip install pre-commit
$ pre-commit install
```
[Указать директорию](.pre-commit-config.yaml) с приложением в которой будут отрабатывать pre-commit хуки:  
```
files: ^(apps/core_dj/|apps/another_app/)
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
Cоздать миграции ("web" - имя контейнера, в котором будут создаваться миграции):
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