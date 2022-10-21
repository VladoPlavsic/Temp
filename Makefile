dev:
	docker-compose up --build

connect:
	docker exec -it `docker ps -a | grep education-platform-backend-server | cut -d ' ' -f 1` bash
