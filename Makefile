# Project
build: ## build
	docker compose build

up: ## up
	docker compose up -d

up-build: ## up-build
	docker compose up --build

down: ## down
	docker compose down

run: ## run
	docker compose build
	docker compose up -d

rebuild: ## rebuild
	docker compose down
	docker compose build
	docker compose up -d

rebuild-frontend: ## rebuild-frontend
	docker compose build frontend
	docker compose up -d frontend

rebuild-backend: ## rebuild-backend
	docker compose down
	docker compose build backend
	docker compose up -d backend

attach-backend: ## attach-backend
	docker attach backend

load-fixtures: ## load-fixtures
	docker-compose exec backend python manage.py loaddata fixtures/sample_emissions.json

attach-frontend: ## attach-frontend
	docker attach frontend
