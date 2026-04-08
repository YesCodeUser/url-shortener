DC = docker compose
APP_CONTAINER = app

DB_SERVICE = postgres
DB_NAME = url_shortener
DB_USER = url_shortener_owner

.PHONY: build up down restart psql init-alembic makemigrations

build:
	$(DC) build

up:
	$(DC) up -d --remove-orphans

down:
	$(DC) down

restart:
	$(DC) restart

psql:
	$(DC) exec $(DB_SERVICE) psql -d $(DB_NAME) -U $(DB_USER)

init-alembic:
	$(DC) exec $(APP_CONTAINER) alembic init -t async migrations

makemigrations:
	$(DC) exec $(APP_CONTAINER) alembic revision --autogenerate -m "$(m)"

migrate:
	$(DC) exec $(APP_CONTAINER) alembic upgrade head

test:
	$(DC) exec $(APP_CONTAINER) pytest -v