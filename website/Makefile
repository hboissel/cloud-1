all: 
	docker compose -f ./srcs/docker-compose.yml build
	docker compose -f ./srcs/docker-compose.yml up -d

logs:
	docker logs wordpress
	docker logs mariadb
	docker logs nginx

stop:
	-docker compose -f ./srcs/docker-compose.yml stop

clean: stop
	-docker compose -f ./srcs/docker-compose.yml down
	-docker compose -f ./srcs/docker-compose.yml rm

fclean: clean
	-rm -rf /home/cloud1/data/mariadb/*
	-rm -rf /home/cloud1/data/wordpress/*
	docker system prune -af

re: fclean all

.Phony: all logs clean fclean
