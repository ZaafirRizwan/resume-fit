.PHONY: dev build up down test lint clean

dev:
	docker-compose up --build

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

test:
	docker-compose run --rm backend pytest

lint:
	docker-compose run --rm backend ruff check .
	docker-compose run --rm backend black --check .

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
