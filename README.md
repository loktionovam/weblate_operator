# Weblate operator

[![weblate operator](https://github.com/loktionovam/weblate_operator/actions/workflows/ci.yml/badge.svg)](https://github.com/loktionovam/weblate_operator/actions/workflows/ci.yml)

[![codecov](https://codecov.io/gh/loktionovam/weblate_operator/branch/master/graph/badge.svg?token=HUQLCJ17SL)](https://codecov.io/gh/loktionovam/weblate_operator)
This is a Kubernetes Operator for the Weblate translation system.

Weblate has a number of components (projects, components, translations) and this operator is designed to simplify creating and managing objects in the Weblate.

Supported versions:

* Weblate >= 4.9

## Building and running

### Prerequisites

* docker engine >= 20.10
* helm >= 3.7.1
* helm-docs >= 1.5.0
* make
* python >= 3.10 (used by tests only)
* python3-venv (used by tests only)
* kind >= 0.14.0

### Setup an environment for developing and testing

* Install prerequisites for developing and testing:

  ```shell
  sudo apt-get install python3-venv
  python3 -m venv venv
  source venv/bin/activate
  python -m pip install --upgrade pip

  # Install for tests only
  pip install -r requirements-test.txt

  # Install for developing
  pip install -r requirements-dev.txt
  ```

### Build and test a docker image

* Set up an image name and tag (optional):

    ```shell
    export WEBLATE_OPERATOR_IMAGE_NAME=yourname/weblate_operator
    export WEBLATE_OPERATOR_IMAGE_TAG=0.1.0
    ```

* Build and test the image:

    ```shell
    make create-cluster
    make build-images
    make test-images
    ```

### Run the weblate_operator

#### Helm

* Install custom resource definitions:

  ```shell
  kubectl apply -f crds
  ```

* Add weblate-operator helm repository:

  ```shell
    helm repo add weblate-operator https://raw.githubusercontent.com/loktionovam/weblate_operator/gh-pages/
    helm repo update
  ```

* Search available weblate-operator helm charts:

  ```shell
    helm search repo --versions weblate-operator

    NAME                             	CHART VERSION	APP VERSION	DESCRIPTION
    weblate-operator/weblate-operator	0.1.0        	v0.1.0     	Weblate operator

  ```

* Deploy new helm release:

  ```shell
  helm install weblate-operator weblate-operator/weblate-operator \
    --version 0.1.0 \
    --set config.weblateAPIUrl="http://weblate.example.com:8080/api/" \
    --set config.weblateAPIKey="secret_api_key"

    helm test weblate-operator
  ```

## Developing and testing weblate operator

* Install prerequisites [as described here](#setup-an-environment-for-developing-and-testing) and activate python virtual environment
* Install pre-commit hooks

  ```shell
  source venv/bin/activate
  pre-commit install
  pre-commit install-hooks
  ```

* Install a k8s cluster:

  ```shell
  make create-cluster
  ```

* Install a weblate helm chart release:

  ```shell
  helm install --set siteDomain=weblate.default.svc.cluster.local --set adminUser=admin --set adminPassword=admin weblate weblate/weblate
  ```

* Obtain an API key in the weblate web interface:

  ```shell
  kubectl port-forward deploy/weblate 8080:8080`
  # Get an API key here http://localhost:8080/
  ```

* Install custom resource definitions:

  ```shell
  kubectl apply -f crds
  ```

* Run the operator:

  ```shell
  export WEBLATE_API_URL=http://localhost:8080/api/
  export WEBLATE_API_KEY=weblate-api-key-here
  kopf run  --verbose -n default  weblate_operator/operator.py
  ```

* Install custom resource examples (a project, a component and translations):

  ```shell
  kubectl apply -f examples
  ```

* Format the code and run tests:

  ```shell
  make fmt
  # tests automatically installs CRDs so delete it first
  kubectl delete -f crds
  make test-apps
  ```
