restart:
	docker compose down
	docker system prune -a -f
	docker compose up

remove-volumes:
	docker system prune -a --volumes -f