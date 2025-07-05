.PHONY: start build makemigration migrate

# Start all services
start:
	docker compose up -d

# Build all services
build:
	docker compose build

# Make migrations for Django backend
migration:
	docker compose exec backend python manage.py makemigrations

# Apply migrations to the database
migrate:
	docker compose exec backend python manage.py migrate