.PHONY: help

IMAGE = low-gas-pay-backend
VERSION ?= $(shell git show -s --pretty=format:%h)

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

image_build: ## Build docker image
	docker build -t $(IMAGE):$(VERSION) .

db_init: ## Init Database
	docker run -it --rm  --name lowgaspay --env FLASK_ENV="DEV" --env FLASK_APP=create_app.py $(IMAGE):$(VERSION) flask db init

db_migrate: ## Migrate Database
	docker run -it --rm  --name lowgaspay --env FLASK_ENV="DEV" --env FLASK_APP=create_app.py $(IMAGE):$(VERSION) flask db migrate && flask db upgrade
