# Project
build: ## build
	docker compose build

up: ## up
	docker compose up -d

up-build: ## up-build
	docker compose up --build

down: ## down
	docker compose down

rebuild: ## rebuild
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

attach-frontend: ## attach-frontend
	docker attach frontend
