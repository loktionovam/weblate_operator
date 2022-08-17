#!/bin/sh

set -euo pipefail

exec /home/weblate_operator/.local/bin/kopf run \
    --log-format=json \
    --liveness=http://0.0.0.0:8080/healthz \
    --namespace="${WEBLATE_OPERATOR_NAMESPACE}" \
    /opt/weblate_operator/operator.py
