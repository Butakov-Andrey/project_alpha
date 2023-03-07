# Project Alpha
Fastapi web-app without frontend frameworks.

## Requirements
To install the required dependencies, run the following commands:
```
$ pip install pip-tools
$ pip-compile ./web/requirements.in
```
## Pre-commit
Install pre-commit to ensure code quality and consistency:
```
$ pip install pre-commit
$ pre-commit install
```
[Specify the app directory](.pre-commit-config.yaml) in which the pre-commit hooks will run:  
```
files: ^(web)
```
[Specify the app directory](.pre-commit-config.yaml) that pre-commit hooks should ignore:  
```
exclude: (?x).*/alembic($|/.*)
```
## Build containers
To set env-file and build the Docker containers, run:
```
$ export ENV_FILE=./example.env
$ docker-compose up -d --build
```

## Database migrations
Create the *web/alembic/versions/* directory and make migrations:  
```
$ docker-compose exec web alembic revision --autogenerate -m "Testing table"
```
Check migrations in *backend/web/alembic/versions/*.  
Upgrade the database:
```
$ docker-compose exec web alembic upgrade head
```
## Testing
Run tests with the following command:  
```
$ docker-compose exec web python -m pytest
```
To check test coverage, run:
```
$ docker-compose exec web coverage run -m pytest
$ docker-compose exec web coverage report -m
```

## TODO:
1. CORS
2. Add logs
3. Static from NGINX
4. Show/hide password in forms
5. GitHub actions
6. lru_cache for settngs