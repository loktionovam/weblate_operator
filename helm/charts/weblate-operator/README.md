# weblate-operator

![Version: 0.1.1](https://img.shields.io/badge/Version-0.1.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: v0.1.1](https://img.shields.io/badge/AppVersion-v0.1.1-informational?style=flat-square)

Weblate Operator

## TL;DR;

```console
$ helm repo add weblate-operator https://raw.githubusercontent.com/loktionovam/weblate_operator/gh-pages/
$ helm repo update

$ helm search repo --versions weblate-operator

 NAME                                   CHART VERSION   APP VERSION     DESCRIPTION
 weblate-exporter/weblate-operator      0.1.2           v0.1.2          Weblate Operator

$  helm install weblate-exporter weblate-exporter/weblate-exporter \
    --set config.weblateAPIUrl="http://weblate.example.com:8080/api/" \
    --set config.weblateAPIKey="secret_api_key"
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| config.weblateAPIKey | string | `""` |  |
| config.weblateAPIUrl | string | `"http://weblate/api/"` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"loktionovam/weblate_operator"` |  |
| image.tag | string | `"v0.1.1"` |  |
| imagePullSecrets | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| projects | list | `[]` |  |
| rbac.create | bool | `true` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8080` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
