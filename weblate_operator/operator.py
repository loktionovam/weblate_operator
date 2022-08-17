import kopf
import weblate.project
import weblate.component
import weblate.translation
import utils
from custom_resource import (
    WeblateProjectCustomResource,
    WeblateComponentCustomResource,
    WeblateTranslationCustomResource,
)


@kopf.on.resume(WeblateProjectCustomResource.plural)
@kopf.on.create(WeblateProjectCustomResource.plural)
def create_project(namespace, body, logger, **kwargs):
    project = weblate.project.WeblateProject(namespace, body, logger)
    resp = project.create()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.update(WeblateProjectCustomResource.plural)
def update_project(namespace, body, logger, **kwargs):
    project = weblate.project.WeblateProject(namespace, body, logger)
    resp = project.update()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.delete(WeblateProjectCustomResource.plural)
def delete_project(namespace, body, logger, **kwargs):
    logger.debug(f"{body = }")
    project = weblate.project.WeblateProject(namespace, body, logger)
    resp = project.delete()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.resume(WeblateComponentCustomResource.plural)
@kopf.on.create(WeblateComponentCustomResource.plural)
def create_component(namespace, body, logger, **kwargs):
    project_name = body.spec.get("weblateProjectName")
    slug = body["spec"]["weblateComponentConfiguration"]["projectSlug"]
    project = utils.KubernetesUtils.get_parent_when_ready(
        project_name, "project", slug, namespace
    )
    utils.KubernetesUtils.adopt(child=dict(body), owner=project)
    component = weblate.component.WeblateComponent(namespace, body, logger)
    resp = component.create()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.update(WeblateComponentCustomResource.plural)
def update_component(namespace, body, logger, **kwargs):
    component = weblate.component.WeblateComponent(namespace, body, logger)
    resp = component.update()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.delete(WeblateComponentCustomResource.plural)
def delete_component(namespace, body, logger, **kwargs):
    component = weblate.component.WeblateComponent(namespace, body, logger)
    resp = component.delete()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.resume(WeblateTranslationCustomResource.plural)
@kopf.on.create(WeblateTranslationCustomResource.plural)
def create_translation(namespace, body, logger, **kwargs):
    component_name = body.spec.get("weblateComponentName")
    slug = body["spec"]["weblateTranslationConfiguration"]["componentSlug"]
    component = utils.KubernetesUtils.get_parent_when_ready(
        component_name, "component", slug, namespace
    )
    utils.KubernetesUtils.adopt(child=dict(body), owner=component)

    translation = weblate.translation.WeblateTranslation(namespace, body, logger)
    resp = translation.create()
    logger.debug(f"{resp = }")
    return resp


@kopf.on.delete(WeblateTranslationCustomResource.plural)
def delete_translation(namespace, body, logger, **kwargs):
    translation = weblate.translation.WeblateTranslation(namespace, body, logger)
    resp = translation.delete()
    logger.debug(f"{resp = }")
    return resp
