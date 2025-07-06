.PHONY: start build makemigration migrate lint lint-fix test lint-ui test-ui

BACKEND_CMD=docker compose exec backend
FRONTEND_CMD=docker compose exec frontend

# Start all services
start:
	docker compose up -d

# Build all services
build:
	docker compose build

# Make migrations for Django backend
migration:
	$(BACKEND_CMD) python manage.py makemigrations

# Apply migrations to the database
migrate:
	$(BACKEND_CMD) python manage.py migrate

# Run Ruff linter on backend code
lint:
	$(BACKEND_CMD) ruff check .

# Run Ruff linter with automatic fixes on backend code
lint-fix:
	$(BACKEND_CMD) ruff check --fix .

test:
	$(BACKEND_CMD) pytest ranked_choice --ds=ranked_choice.settings -v

lint-ui:
	$(FRONTEND_CMD) npm run lint-fix && $(FRONTEND_CMD) npm run format

test-ui:
	$(FRONTEND_CMD) npm run test
