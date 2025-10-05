.PHONY: up down logs migrate revision seed fmt test

up:
\tdocker compose up -d

down:
\tdocker compose down -v

logs:
\tdocker compose logs -f board-api

revision:
\tcd .. && docker compose exec board-api alembic revision -m "$(m)" --autogenerate

migrate:
\tcd .. && docker compose exec board-api alembic upgrade head

fmt:
\tcd .. && docker compose exec board-api bash -lc "black . && isort ."

seed:
\tcd .. && docker compose exec board-api python app/db/seed.py
