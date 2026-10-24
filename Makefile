restart:
	docker compose down
	docker system prune -a -f
	docker compose up

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