all: help

help:				## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

# Application
# ----------------------------------------------------------------------------------------------------------------------
install:			## Run install script => requirements, migrate, load fixtures, createsuperuser
	@./scripts/install.sh

requirements:			## Install requirements for running
	@pip install -r config/requirements/app.pip

requirements-all:		## Install requirements for running, building and deploying
	@pip install -r config/requirements/app.pip
	@pip install -r config/requirements/build.pip
	@pip install -r config/requirements/deploy.pip

runserver:			## Run server on localhost:8000
	@./manage.py runserver localhost:8000

fakeusers:			## Create fake users, store them in DB => 3 admins, 8 mentors, 20 trainees
	@./manage.py createfakeusers 20 --prefix Trainee --role trainee
	@./manage.py createfakeusers 8 --prefix Mentor --role mentor
	@./manage.py createfakeusers 3 --prefix Admin --role admin

pylint:				## Run pylint scanning
	@./scripts/run-pylint.sh

tests:				## Run tests with coverage
	@coverage erase
	@coverage run --branch --source='.' manage.py test
	@coverage report -m

build:				## Run tests, pylint
build: tests pylint



# Docker-compose
# ----------------------------------------------------------------------------------------------------------------------
docker-ps:			## Show container names, status, ports
	@docker ps -a --format="table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

docker-logs:			## Show docker logs
	@docker-compose logs -f

docker-build:			## Build docker containers
	@docker-compose build

docker-up:			## Up docker containers in background
	@docker-compose up -d
	@docker-compose logs -f

docker-build-up:		## Build and up docker containers in background
docker-build-up: docker-build docker-up

docker-stop:			## Stop docker containers
	@docker-compose stop

docker-down:			## Down docker containers(stop, remove networks)
	@docker-compose down

docker-rebuild:			## Rebuild containers(down, build, up)
docker-rebuild: docker-down	docker-build-up

.ONESHELL:
docker-bash:			## Open bash in container with entered name
	@echo "Container names: "
	@docker ps -a --format="{{.Names}}"
	@read -p 'Enter container name: ' container_name
	@docker exec -it $$container_name sh -c "export DOCKER_ENABLE='True' && bash"
