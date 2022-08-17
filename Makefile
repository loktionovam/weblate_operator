WEBLATE_OPERATOR_IMAGE_NAME ?= loktionovam/weblate_operator
WEBLATE_OPERATOR_IMAGE_TAG ?= $(shell ./get_version.sh)
GIT_BRANCH_NAME := $(shell git branch  --show-current)
export

lint:
	python -m black --check weblate_operator tests

test-apps: lint
	python -m pytest --cov-report=xml --cov-report=term --cov=weblate_operator tests/apps -v

fmt:
	python -m black weblate_operator tests

build-images:
	docker build --build-arg VERSION=$(WEBLATE_OPERATOR_IMAGE_TAG) -t $(WEBLATE_OPERATOR_IMAGE_NAME):$(WEBLATE_OPERATOR_IMAGE_TAG) .
	docker tag $(WEBLATE_OPERATOR_IMAGE_NAME):$(WEBLATE_OPERATOR_IMAGE_TAG) $(WEBLATE_OPERATOR_IMAGE_NAME):dev

test-images:
	python -m pytest tests/images -v

push-images:
	docker push $(WEBLATE_OPERATOR_IMAGE_NAME):$(WEBLATE_OPERATOR_IMAGE_TAG)
	docker push $(WEBLATE_OPERATOR_IMAGE_NAME):dev

build-charts:
	helm lint helm/charts/weblate-operator
	helm/release_helm_chart.py

create-cluster:
	kind create cluster --name weblate-operator
	kubectl cluster-info --context kind-weblate-operator

delete-cluster:
	kind delete cluster --name weblate-operator

changelog:
ifeq ($(GIT_BRANCH_NAME), main)
	@echo "Current branch is $(GIT_BRANCH_NAME), create changelog"
	gitchangelog > CHANGELOG.md
else
	@echo "Current branch is $(GIT_BRANCH_NAME), skipping to update CHANGELOG.md"
endif

all: test-apps build-images test-images build-charts

# build-charts
.PHONY: test-apps fmt lint build-images test-images push-images create-cluster delete-cluster all
