all: up

up:
	docker-compose -f ./srcs/docker-compose.yml up -d --remove-orphans

ps:
	cd ./srcs/ && docker-compose ps -a

down:
	docker-compose -f ./srcs/docker-compose.yml down

stop:
	cd ./srcs/ && docker-compose stop

# logs:
# 	docker-compose logs "CONTENAIR ID du docker dont tu veux le logs"

clean:
	cd ./srcs/ && docker-compose stop 
	cd ./srcs/ && docker-compose down -v

fclean: clean
	docker system prune --all

.PHONY: up data db wp down
