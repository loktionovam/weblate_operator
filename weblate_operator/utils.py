import kopf
import kubernetes
from kubernetes.client.rest import ApiException
from custom_resource import WeblateAllCustomResources


class KubernetesUtils:
    @staticmethod
    def get_custom_resource_fields(resource):
        with kubernetes.client.ApiClient() as api_client:
            api_instance = kubernetes.client.ApiextensionsV1Api(api_client)
        try:
            crd_list = api_instance.list_custom_resource_definition()
            kind = resource["kind"]
            for item in crd_list.items:
                if item._spec._names.kind == kind:
                    group = item._spec.group
                    plural = item._spec._names.plural

            name = resource["metadata"]["name"]
            version = resource["apiVersion"].split("/")[-1]
            return {"name": name, "version": version, "group": group, "plural": plural}
        except ApiException as e:
            print(
                "Exception when calling ApiextensionsV1Api->get_api_resources: %s\n" % e
            )
            return {}

    @staticmethod
    def get_namespaced_custom_resource_fields(resource):
        result = KubernetesUtils.get_custom_resource_fields(resource)
        result["namespace"] = resource["metadata"]["namespace"]
        return result

    @staticmethod
    def adopt(child, owner):
        child_fields = KubernetesUtils.get_namespaced_custom_resource_fields(child)
        with kubernetes.client.ApiClient() as api_client:
            api_instance = kubernetes.client.CustomObjectsApi(api_client)
        kopf.adopt(child, owner=owner)
        patch = {"metadata": {"ownerReferences": child["metadata"]["ownerReferences"]}}

        resp = api_instance.patch_namespaced_custom_object(
            child_fields["group"],
            child_fields["version"],
            child_fields["namespace"],
            child_fields["plural"],
            child_fields["name"],
            body=patch,
        )
        return resp

    @staticmethod
    def get_parent_when_ready(parent_name, parent_type, slug, namespace):
        ParentCustomResource = WeblateAllCustomResources.get_custom_resource(
            search=parent_type
        )
        parent_name_cap = parent_name.capitalize()
        parent_type_cap = parent_type.capitalize()
        try:
            parent = ParentCustomResource(name=parent_name, namespace=namespace).get()
            status = parent["status"][f"create_{parent_type}"]

            try:
                if status["slug"] != slug:
                    raise kopf.PermanentError(
                        "The {slug} is not equal to {parent_type} slug in {parent_type}."
                    )
            except IndexError:
                raise kopf.TemporaryError(
                    f"Weblate{parent_name_cap} {parent_name} has been created but {parent_type} information is empty",
                    delay=30,
                )
        except (kubernetes.client.exceptions.ApiException, IndexError, KeyError) as err:
            print(err)
            raise kopf.TemporaryError(
                f"Weblate{parent_type_cap} {parent_name} is not created yet", delay=10
            )
        return parent
