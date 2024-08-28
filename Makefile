all:
	docker compose -f docker-compose.yml up --build -d 

logs:
	docker logs ansible

stop:
	docker compose -f docker-compose.yml stop 

clean: stop
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml rm

re: clean all

ansible:
	docker exec -it ansible /bin/bash

.PHONY: all ansible logs clean fclean