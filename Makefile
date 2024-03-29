NAME = app
DEV_COMPOSE_FILE	= docker-compose.yml
STAGING_COMPOSE_FILE= docker-compose.staging.yml
PROD_COMPOSE_FILE	= docker-compose.prod.yml
LOCAL_URL			= http://localhost:8000
URL					= https://www.dreamteampong.pro

all: build run
dev: build-dev run-dev
staging: build-staging run-staging

# Build the docker images in the docker-compose.yml file
build:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run"

build-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run"

build-staging:
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run"


# Run the docker containers in the docker-compose.yml file
run:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now starting on ${URL}"

run-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now starting on ${LOCAL_URL}"

run-staging:
	sudo docker-compose -f $(STAGING_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now starting on ${URL}"


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
del-containers:
	@if [ -n "$$(sudo docker ps -aq)" ]; then 		\
		sudo docker rm -f $$(sudo docker ps -aq);	\
	fi
	@if [ -n "$$(sudo docker images -q)" ];					\
		then sudo docker rmi -f $$(sudo docker images -q);	\
	fi
	@if [ -n "$$(sudo docker volume ls -q)" ];	\
		then sudo docker volume prune -f;		\
	fi

fclean: clean del-containers

fclean-dev: clean-dev del-containers

fclean-staging: clean-staging del-containers


re: fclean all

re-dev: fclean-dev dev

re-staging: fclean-staging staging

.PHONY: all dev staging build build-dev build-staging run run-dev run-staging stop stop-dev stop-staging clean clean-dev clean-staging fclean fclean-dev fclean-staging re re-dev re-staging
