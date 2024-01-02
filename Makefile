#!/usr/bin/make -f

DC = srcs/docker-compose.yaml
ENV = srcs/.env

# env Virtual Machine
# DATA_DIR = /home/$(USER)/data

# env WSL 
# change groot by your hostname
DATA_DIR = /home/groot/data

# Make
all: init frontend backend elk

frontend:
	@docker-compose -f $(DC) --env-file $(ENV) up --detach caddy website

backend:
	@docker-compose -f $(DC) --env-file $(ENV) up --detach db backend prom graf

elk:
	@docker-compose -f $(DC) --env-file $(ENV) up --detach elastic logs kib db backend

# ---------------------------------------------------------------

build:
	@docker-compose -f $(DC) --env-file $(ENV) up --detach --build

build_frontend:
	@docker-compose -f $(DC) --env-file $(ENV) build caddy website

build_backend:
	@docker-compose -f $(DC) --env-file $(ENV) build db backend prom graf

build_elk:
	@docker-compose -f $(DC) --env-file $(ENV) build elastic logs kib db backend

# ---------------------------------------------------------------

volumes:
	@mkdir -p $(DATA_DIR)/{db,back,website,elastic,graf,kib,logs}

volumes_frontend:
	@mkdir -p $(DATA_DIR)/{website,caddy_data,caddy_config}

volumes_backend:
	@mkdir -p $(DATA_DIR)/{db,back,prom,graf}

volumes_elk:
	@mkdir -p $(DATA_DIR)/{elastic,logs,kib, db backend}

# ---------------------------------------------------------------

stop: 
	@docker-compose -f $(DC) --env-file $(ENV) stop

stop_frontend:
	@docker-compose -f $(DC) --env-file $(ENV) stop caddy website
	@docker-compose -f $(DC) --env-file $(ENV) rm -f caddy website

stop_backend:
	@docker-compose -f $(DC) --env-file $(ENV) stop db backend prom graf
	@docker-compose -f $(DC) --env-file $(ENV) rm -f db backend prom graf

stop_elk:
	@docker-compose -f $(DC) --env-file $(ENV) stop elastic logs kib db backend
	@docker-compose -f $(DC) --env-file $(ENV) rm -f elastic logs kib db backend

# ---------------------------------------------------------------

down:
	@docker-compose -f $(DC) --env-file $(ENV) down

down_frontend:
	@docker-compose -f $(DC) --env-file $(ENV) down caddy website

down_backend:
	@docker-compose -f $(DC) --env-file $(ENV) down db backend prom graf

down_elk:
	@docker-compose -f $(DC) --env-file $(ENV) down elastic logs kib db backend

# ---------------------------------------------------------------

restart_all:
	@docker-compose -f $(DC) --env-file $(ENV) down
	@docker-compose -f $(DC) --env-file $(ENV) up -d

restart_frontend:
	@docker-compose -f $(DC) --env-file $(ENV) restart caddy website

restart_backend:
	@docker-compose -f $(DC) --env-file $(ENV) restart db backend prom graf

restart_elk:
	@docker-compose -f $(DC) --env-file $(ENV) restart elastic logs kib db backend

# ---------------------------------------------------------------

fclean:
	@if [ $$(docker ps -q | wc -l) -gt 0 ]; then \
		docker stop $$(docker ps -aq); \
	fi
	@docker system prune -af --volumes
	@sudo rm -rf $(DATA_DIR)


re: fclean all

.PHONY: frontend backend elk all build volumes stop down fclean re
