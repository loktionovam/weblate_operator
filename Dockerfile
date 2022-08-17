FROM python:3-alpine as weblate_operator

ARG VERSION=dev
RUN adduser -S -D -u 1000 weblate_operator
USER weblate_operator

LABEL maintainer=loktionovam@gmail.com
LABEL version=${VERSION}
ENV WEBLATE_OPERATOR_NAMESPACE=default \
    WEBLATE_API_URL=http://weblate:8080/api/ \
    WEBLATE_API_KEY=

COPY requirements.txt entrypoint.sh /opt/

RUN pip install --no-cache-dir -r /opt/requirements.txt
COPY weblate_operator /opt/weblate_operator
ENTRYPOINT ["/opt/entrypoint.sh"]

FROM weblate_operator AS vulnscan
COPY --from=aquasec/trivy:latest /usr/local/bin/trivy /usr/local/bin/trivy
USER root
RUN trivy rootfs --exit-code 1 --no-progress --skip-files /usr/local/bin/trivy /

FROM weblate_operator as main
