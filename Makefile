.PHONY: build up down restart logs shell migrate makemigrations \
        createsuperuser test lint collectstatic

# Construção e execução
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f web

logs-worker:
	docker compose logs -f celery_worker

# Django
shell:
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

makemigrations-app:
	docker compose exec web python manage.py makemigrations $(app)

createsuperuser:
	docker compose exec web python manage.py createsuperuser

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

# Banco de dados
db-shell:
	docker compose exec db psql -U $${DB_USER} -d $${DB_NAME}

db-reset:
	docker compose down -v
	docker compose up -d db

# Qualidade de código
lint:
	docker compose exec web flake8 apps/ core/ config/

test:
	docker compose exec web python manage.py test apps/

# Setup inicial completo
setup: build up migrate createsuperuser
	@echo "Sistema configurado com sucesso."

# Tailwind
tailwind-watch:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

tailwind-build:
	npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

css-build:
	./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify

css-watch:
	./tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch