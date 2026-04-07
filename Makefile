DC = docker compose
APP_CONTAINER = url-shortener

DB_SERVICE = postgres
DB_NAME = url_shortener
DB_USER = url_shortener_owner

up:
	$(DC) up -d --remove-orphans

down:
	$(DC) down

restart:
	$(DC) restart

psql:
	$(DC) exec $(DB_SERVICE) psql -d $(DB_NAME) -U $(DB_USER)

