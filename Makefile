
GIT_EMAIL_CONFIG = $(shell git config --get user.email || echo "")
GIT_USER_CONFIG = $(shell git config --get user.name || echo "")

graph_models:
	python ./manage.py graph_models -a -g -o docs/core_models.png

docker_build:
	docker buildx build --platform linux/amd64 --provenance=false --build-arg GIT_COMMIT=$(git log -1 --format=%h)[$(date '+%Y-%m-%d%H:%M:%S')] -t rfc/core -f compose/production/django/Dockerfile --no-cache .

docker_tag:
	docker tag rfc/core:latest 727646490686.dkr.ecr.us-east-1.amazonaws.com/rfc/core:latest

docker_push:
	docker push 727646490686.dkr.ecr.us-east-1.amazonaws.com/rfc/core:latest

docker_deploy: docker_build docker_tag docker_push

dev_install:
	git config --global http.github.com.sslVerify false
	git config --global pull.rebase false
	@echo "Checking git user.email configuration..."
	@if [ -z "$(strip $(GIT_EMAIL_CONFIG))" ]; then \
		echo "Error: git user.email is not configured."; \
		echo -n "Enter your email: " && read GIT_EMAIL_CONFIG; \
		git config --global user.email "$$GIT_EMAIL_CONFIG"; \
		echo "git user.email is set to: $$GIT_EMAIL_CONFIG"; \
	else \
		echo "git user.email is set to: $(GIT_EMAIL_CONFIG)"; \
	fi
	@echo "Checking git user.name configuration..."
	@if [ -z "$(strip $(GIT_USER_CONFIG))" ]; then \
		echo "Error: git user.name is not configured."; \
		echo -n "Enter your name: " && read GIT_USER_CONFIG; \
		git config --global user.name "$$GIT_USER_CONFIG"; \
		echo "git user.name is set to: $$GIT_USER_CONFIG"; \
	else \
		echo "git user.name is set to: $(GIT_USER_CONFIG)"; \
	fi
	touch .env
	docker compose up oracle-db -d
	docker compose cp compose/local/oracle/install.sql oracle-db:/tmp/install.sql
	docker compose exec -T oracle-db sqlplus -s / as sysdba @/tmp/install.sql
	docker compose exec -T django python3.13 /srv/manage.py migrate
	docker compose exec -T django python3.13 /srv/manage.py migrate_dynamodb


reset_tables:
	rm -f ./core/general/migrations/0*.py ./core/tariff/migrations/0*.py ./core/ticket/migrations/0*.py ./core/refunds/migrations/0*.py ./core/revenue/migrations/0*.py
	docker compose up oracle-db -d
	docker compose cp compose/local/oracle/clear_tables.sql oracle-db:/tmp/clear_tables.sql
	docker compose exec -T oracle-db sqlplus -s / as sysdba @/tmp/clear_tables.sql

clean:
	@echo "Cleaning"
	git reset --hard
