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
	docker compose down
	docker compose build
	docker compose up -d

attach-backend: ## attach-backend
	docker attach backend

attach-frontend: ## attach-frontend
	docker attach frontend
