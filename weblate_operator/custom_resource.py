import kubernetes


class WeblateCustomResource:
    group = "loktionovam.com"
    version = "v1alpha1"

    def __init__(self, name, namespace, plural):
        self.namespace = namespace
        self.name = name
        self._api = kubernetes.client.CustomObjectsApi()
        self.plural = plural

    def get(self):
        resource = self._api.get_namespaced_custom_object(
            group=WeblateCustomResource.group,
            version=WeblateCustomResource.version,
            namespace=self.namespace,
            plural=self.plural,
            name=self.name,
        )
        return resource


class WeblateProjectCustomResource(WeblateCustomResource):
    kind = "WeblateProject"
    plural = "weblateprojects"
    short = "project"

    def __init__(self, name, namespace):
        super().__init__(name, namespace, WeblateProjectCustomResource.plural)


class WeblateComponentCustomResource(WeblateCustomResource):
    kind = "WeblateComponent"
    plural = "weblatecomponents"
    short = "component"

    def __init__(self, name, namespace):
        super().__init__(name, namespace, WeblateComponentCustomResource.plural)


class WeblateTranslationCustomResource(WeblateCustomResource):
    kind = "WeblateTranslation"
    plural = "weblatetranslations"
    short = "translation"

    def __init__(self, name, namespace):
        super().__init__(name, namespace, WeblateTranslationCustomResource.plural)


class WeblateAllCustomResources:
    data = (
        WeblateProjectCustomResource,
        WeblateComponentCustomResource,
        WeblateProjectCustomResource,
    )

    @staticmethod
    def get_custom_resource(search, search_field="short"):
        for resource in WeblateAllCustomResources.data:
            if getattr(resource, search_field) == search:
                return resource
        raise Exception(f"Can't find custom resource {search}")


if __name__ == "__main__":
    from kubernetes.config import load_kube_config

    load_kube_config()
    cr = WeblateAllCustomResources.get_custom_resource(search="project")
    print(type(cr))
