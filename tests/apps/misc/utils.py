import yaml
from kubernetes.config import load_kube_config
from kubernetes.dynamic.client import DynamicClient
from kubernetes.client import api_client


class KubernetesManifestRunner:
    def __init__(self, path):
        load_kube_config()

        self.client = DynamicClient(api_client.ApiClient())
        self.path = path
        self._api, self._manifest, self._namespace, self._name = self._load_resource()

    def _load_resource(self):

        with open(self.path) as manifest_file:
            manifest = yaml.safe_load(manifest_file)

        api_version = manifest["apiVersion"].split("/")[-1]
        kind = manifest["kind"]
        name = manifest["metadata"]["name"]
        try:
            namespace = manifest["metadata"]["namespace"]
        except KeyError:
            namespace = "default"

        try:
            api = self.client.resources.get(
                api_version=api_version, kind=kind, namespace=namespace
            )
        except AttributeError as err:
            if "object has no attribute 'namespace'" in str(err):
                api = self.client.resources.get(api_version=api_version, kind=kind)

        return api, manifest, namespace, name

    def create(self):
        return self._api.create(self._manifest, namespace=self._namespace)

    def delete(self):
        return self._api.delete(self._name, namespace=self._namespace)

    def get(self):
        return self._api.get(name=self._name, namespace=self._namespace)

    def patch(self, body):
        self._api.patch(
            body=body,
            name=self._name,
            namespace=self._namespace,
            content_type="application/merge-patch+json",
        )
