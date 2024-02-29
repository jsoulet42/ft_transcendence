NAME = app
DEV_COMPOSE_FILE	= docker-compose.yml
STAGING_COMPOSE_FILE= docker-compose.staging.yml
PROD_COMPOSE_FILE	= docker-compose.prod.yml
URL					= www.dreamteampong.pro

all: build run
dev: build-dev run-dev
staging: build-staging run-staging

# Build the docker images in the docker-compose.yml file
build:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run on https://${URL}"

build-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run on https://${URL}"

build-staging:
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run on https://${URL}"


# Run the docker containers in the docker-compose.yml file
run:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now running on https://${URL}"

run-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now running on https://${URL}"

run-staging:
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now running on https://${URL}"


stop:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) stop

stop-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) stop

stop-staging:
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) stop


# Launch the tests
test: build run

test-dev: build-dev run-dev

test-staging: build-staging run-staging


# Stop and remove the docker containers
clean: stop
	sudo docker-compose -f $(PROD_COMPOSE_FILE) down -v

clean-dev: stop-dev
	sudo docker-compose -f $(DEV_COMPOSE_FILE) down -v

clean-staging: stop-staging
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) down -v


# Remove the docker images
fclean: clean
	@if [ -n "$$(sudo docker ps -a -q)" ]; then sudo docker rm -f $$(sudo docker ps -a -q); fi
	@if [ -n "$$(sudo docker images -q)" ]; then sudo docker rmi -f $$(sudo docker images -q); fi
	@if [ -n "$$(sudo docker volume ls -q)" ]; then sudo docker volume prune -f; fi

fclean-dev: clean-dev
	@if [ -n "$$(sudo docker ps -a -q)" ]; then sudo docker rm -f $$(sudo docker ps -a -q); fi
	@if [ -n "$$(sudo docker images -q)" ]; then sudo docker rmi -f $$(sudo docker images -q); fi
	@if [ -n "$$(sudo docker volume ls -q)" ]; then sudo docker volume prune -f; fi

fclean-staging: clean-staging
	@if [ -n "$$(sudo docker ps -a -q)" ]; then sudo docker rm -f $$(sudo docker ps -a -q); fi
	@if [ -n "$$(sudo docker images -q)" ]; then sudo docker rmi -f $$(sudo docker images -q); fi
	@if [ -n "$$(sudo docker volume ls -q)" ]; then sudo docker volume prune -f; fi


re: fclean all

re-dev: fclean-dev dev

re-staging: fclean-staging staging

.PHONY: all dev staging build build-dev build-staging run run-dev run-staging stop stop-dev stop-staging clean clean-dev clean-staging fclean fclean-dev fclean-staging re re-dev re-staging
