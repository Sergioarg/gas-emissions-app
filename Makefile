# Project
build: ## build
	docker compose build

up: ## up
	docker compose up -d

up-build: ## up-build
	docker compose up --build

down: ## down
	docker compose down

re-build: ## re-build
	docker compose down
	docker compose build
	docker compose up -d
