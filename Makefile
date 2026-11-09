NETWORK_NAME=shared-auth-network

restart:
	docker compose down --remove-orphans
	docker compose up --build

restart-authentik:
	docker compose -p authentik -f docker-compose.authentik.yml down --remove-orphans
	docker system prune -a -f
	docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || docker network create $(NETWORK_NAME)
	docker compose -p authentik -f docker-compose.authentik.yml up --build -d

remove-volumes:
	docker system prune -a --volumes -f

revision:
	@read -p "Enter migration description: " msg; \
	alembic revision --autogenerate -m "$$msg"

up:
	alembic upgrade head

down:
	alembic downgrade -1

format:
	ruff format .
	cd client && npx prettier --write "**/*.{js,jsx,css,json}"

rebuild-api-image:
	docker compose up -d --force-recreate api

rebuild-client-image:
	docker compose up -d --force-recreate client