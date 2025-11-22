makemigrations:  ## makemigrations
	docker compose run --rm --entrypoint=python3 worker manage.py makemigrations

migrate: ## migrate
	docker compose run --rm --entrypoint=python3 worker manage.py migrate

reset-db: ## reset_db
	docker compose run --rm --entrypoint=python3 worker manage.py reset_db -c

shell: ## shell
	docker compose run --rm --entrypoint=python3 worker manage.py shell_plus

run-tests:  # run-tests
	docker compose run --rm --entrypoint=pytest worker /mo_services/tests/ ${args}
