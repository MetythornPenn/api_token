down:
	docker compose down

up:
	docker compose -d 

build:
	docker compose up -d --build

logs:
	docker compose logs -f

ps:
	docker ps

images:
	docker images 