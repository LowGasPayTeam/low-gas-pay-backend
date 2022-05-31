.PHONY: help

REPO ?= lowgaspay
APP ?= low-gas-pay-backend
VERSION ?= $(shell git show -s --pretty=format:%h)
IMAGE = $(APP):$(VERSION)

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

app_build: ## Build docker image
	docker build -t $(IMAGE) .

app_push: ## Push docker image
	docker tag  $(IMAGE) $(REPO)/$(IMAGE)
	docker push $(REPO)/$(IMAGE)

db_init: ## Init Database
	docker run -it --rm  --name lowgaspay --env FLASK_ENV="DEV" --env FLASK_APP=create_app.py $(IMAGE) flask db init

db_migrate: ## Migrate Database
	docker run -it --rm  --name lowgaspay --env FLASK_ENV="DEV" --env FLASK_APP=create_app.py $(IMAGE) flask db migrate && flask db upgrade

app_run: ## Run low-gas-pay-backend
	docker run -d --name lowgaspay --env FLASK_ENV="DEV" $(IMAGE)
