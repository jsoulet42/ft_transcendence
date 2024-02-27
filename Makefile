NAME = app
DEV_COMPOSE_FILE	= docker-compose.yml
PROD_COMPOSE_FILE	= docker-compose.prod.yml
URL					= www.dreamteampong.pro

all: build run

# Build the docker images in the docker-compose.yml file
build:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run on https://${URL}"

build-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) build
	@echo "\n\nTranscendence is now built and ready to run on https://${URL}"


# Run the docker containers in the docker-compose.yml file
run:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now running on https://${URL}"

run-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) up -d
	@echo "\n\nTranscendence is now running on https://${URL}"


ssl-certificate:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email souletjulien42@gmail.com --agree-tos --no-eff-email -d dreamteampong.pro -d www.dreamteampong.pro


stop:
	sudo docker-compose -f $(PROD_COMPOSE_FILE) stop

stop-dev:
	sudo docker-compose -f $(DEV_COMPOSE_FILE) stop


# Launch the tests
test: build run

test-dev: build-dev run-dev


# Stop and remove the docker containers
clean: stop
	sudo docker-compose -f $(PROD_COMPOSE_FILE) down -v

cleaan-dev: stop-dev
	sudo docker-compose -f $(DEV_COMPOSE_FILE) down -v


# Remove the docker images
fclean: clean
	@if [ -n "$$(sudo docker ps -a -q)" ]; then sudo docker rm -f $$(sudo docker ps -a -q); fi
	@if [ -n "$$(sudo docker images -q)" ]; then sudo docker rmi -f $$(sudo docker images -q); fi
	@if [ -n "$$(sudo docker volume ls -q)" ]; then sudo docker volume prune -f; fi

fclean-dev: clean-dev
	@if [ -n "$$(sudo docker ps -a -q)" ]; then sudo docker rm -f $$(sudo docker ps -a -q); fi
	@if [ -n "$$(sudo docker images -q)" ]; then sudo docker rmi -f $$(sudo docker images -q); fi
	@if [ -n "$$(sudo docker volume ls -q)" ]; then sudo docker volume prune -f; fi


re: fclean all

re-dev: fclean-dev build-dev run-dev

.PHONY: all build build-dev run run-dev stop stop-dev clean clean-dev fclean fclean-dev re re-dev
