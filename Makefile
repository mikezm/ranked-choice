.PHONY: start build makemigration migrate lint lint-fix

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

# Run Ruff linter on backend code
lint:
	docker compose exec backend ruff check .

# Run Ruff linter with automatic fixes on backend code
lint-fix:
	docker compose exec backend ruff check --fix .
