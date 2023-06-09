.DEFAULT_GOAL := help
.PHONY: help
.EXPORT_ALL_VARIABLES:

include .env

pre:
	pre-commit run --all-files
cov:
	pytest --cov=src --cov-report term-missing


# Docker
ps: 
	docker-compose ps --all		

up: 
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

prune: confirm
	docker system prune --all --force --volume
	docker volume rm $(shell docker volume ls -qf dangling=true)

image:
	docker compose -f docker-compose.yml -f docker

reload: down up
reset: down prune up

db_shell:
	docker exec -it postgres_container psql -U ${POSTGRES_USER} -d ${POSTGRES_DBNAME}