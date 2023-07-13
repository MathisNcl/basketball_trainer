.DEFAULT_GOAL := help
.PHONY: help
.EXPORT_ALL_VARIABLES:

include .env
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 _]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Code 
deps: # Install deps
	pip install -e .[all]
pre: # Run pre-commit hooks on all files
	pre-commit run --all-files
cov: # Compute coverage
	pytest --cov=src --cov-report term-missing --headless

report: # Make report cov
	tox -r

# Docker
ps: # Show all current Docker
	docker-compose ps --all		

up: # Up Postgres Docker
	docker-compose up -d

down: # Down Postgres Docker
	docker-compose down

docker_remove:
	docker volume rm bball_pgdata

restart: # Restart Postgres Docker
	docker-compose restart

image: # Run Docker Compose
	docker compose -f docker-compose.yml -f docker

reload: down up # Run Make down and Make up

db_shell: # Lunch an interactive shell inside the Docker Postgres
	docker exec -it postgres_container psql -U ${POSTGRES_USER} -d ${POSTGRES_DBNAME}

# API
api_run : # Run FastApi main.py
	uvicorn src.bball_trainer.api.main:app --reload

# dashboard
dash_run: # Run Dash app.py
	python src/bball_trainer/dashboard/app.py

new_terminal: # Open a terminal
	open -a Terminal 
