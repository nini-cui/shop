restart:
	docker compose down
	docker system prune -a -f
	docker compose up --build

restart-authentik:
	docker compose -p authentik -f docker-compose.authentik.yml down
	docker system prune -a -f
	docker compose -p authentik -f docker-compose.authentik.yml up --build

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