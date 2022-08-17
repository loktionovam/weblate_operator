from . import client as wc
from abc import ABC, abstractmethod
from wlc import WeblateException
import kubernetes


class WeblateAbstract(ABC):
    def __init__(self, namespace, plural, body):
        self.weblate = wc.WeblateClient().get_client()
        self.namespace = namespace
        self.metadata = body["metadata"]
        self.spec = body["spec"]
        self.body = body
        self.resource_group, self.resource_version = self.body["apiVersion"].split("/")
        self.resource_plural = plural
        self.resource_name = self.body["metadata"]["name"]
        self.resource_status = {
            "status": {
                "message": "",
            }
        }
        self.api_path = None
        self.logger = None

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    # FIXME: move this method to custom_resources
    def update_status(self, message=""):
        self.resource_status = {
            "status": {
                "message": message,
            }
        }

        try:
            api = kubernetes.client.CustomObjectsApi()
            api_response = api.patch_namespaced_custom_object(
                self.resource_group,
                self.resource_version,
                self.namespace,
                self.resource_plural,
                self.resource_name,
                body=self.resource_status,
            )
            self.logger.info(api_response)
        except kubernetes.client.rest.ApiException as e:
            print(
                "Exception when calling CustomObjectsApi->patch_namespaced_custom_object: %s\n"
                % e
            )
