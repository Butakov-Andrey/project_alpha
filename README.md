# Project Alpha
Проект реализован в виде монорепозитория для микросервисов backend и frontend  

Установить pip-tools, создать requirements.txt и установить зависимости  
(необходимо находиться в директории с *requirements.in*):
```
$ pip install pip-tools
$ pip-compile
$ pip-sync
```
Установить pre-commit хуки:
```
$ pip install pre-commit
$ pre-commit install
```
[Указать директорию](.pre-commit-config.yaml) с приложением в которой будут отрабатывать pre-commit хуки:  
```
files: ^(web)
```
И [директорию](.pre-commit-config.yaml), которую pre-commit хуки должны игнорировать:
```
exclude: (?x).*/alembic($|/.*)
```
Создание образов и запуск контейнеров:
```
$ docker-compose up -d --build
```

## Web
Создать директорию *web/alembic/versions/*  
Cоздать миграции ("web" - имя контейнера, в котором будут создаваться миграции):
```
$ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Проверить сгенерированные миграции в директории *backend/web/alembic/versions/*  
Применить миграции и обновить базу данных:
```
$ docker-compose exec web alembic upgrade head
```

## TODO:
id поменять на uuid

## Notes:

docker-compose exec web coverage report -m 

docker-compose exec web python -m pytest -s