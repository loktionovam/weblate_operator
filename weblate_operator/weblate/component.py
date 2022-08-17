from . import WeblateAbstract
from wlc import WeblateException


class WeblateComponent(WeblateAbstract):
    def __init__(self, namespace, body, logger):
        super().__init__(namespace, "weblatecomponents", body)
        self.project_slug = self.spec["weblateComponentConfiguration"]["projectSlug"]
        self.name = self.spec["weblateComponentConfiguration"]["name"]
        self.slug = self.spec["weblateComponentConfiguration"]["slug"]
        self.file_format = self.spec["weblateComponentConfiguration"]["fileFormat"]
        self.filemask = self.spec["weblateComponentConfiguration"]["fileMask"]
        self.repo = self.spec["weblateComponentConfiguration"]["repo"]
        self.vcs = self.spec["weblateComponentConfiguration"]["vcs"]
        self.branch = self.spec["weblateComponentConfiguration"]["branch"]
        self.new_base = self.spec["weblateComponentConfiguration"]["newBase"]
        self.info = (
            f"name: {self.name}, slug: {self.slug}, project_slug: {self.project_slug}"
        )
        self.logger = logger
        self.component_path = f"{self.project_slug}/{self.slug}"
        self.api_path = f"components/{self.component_path}/"

    def create(self):
        try:
            resp = self.weblate.create_component(
                name=self.name,
                slug=self.slug,
                project=self.project_slug,
                file_format=self.file_format,
                filemask=self.filemask,
                repo=self.repo,
                vcs=self.vcs,
                branch=self.branch,
                new_base=self.new_base,
            )
            message = f"Component is created {self.info}"
            self.logger.info(message)
            self.update_status(message)
            return resp
        except WeblateException as err:
            error_msg = str(err)
            if "HTTP error 400" in error_msg and "already exist" in error_msg:
                return self.update()
            else:
                raise err

    def delete(self):
        retention_policy = self.spec["weblateComponentRetentionPolicy"]["whenDeleted"]
        self.logger.info(f"Weblate component retention policy: {retention_policy}")

        if retention_policy == "Delete":

            try:
                weblate_component = self.weblate.get_component(path=self.component_path)
                resp = weblate_component.delete()
                self.logger.info(f"Component is deleted {self.info}")
                return resp
            except Exception as err:
                self.logger.error(err)

    def update(self):
        try:
            resp = self.weblate.request(
                "patch",
                path=f"{self.api_path}",
                data={"name": self.name, "repo": self.repo},
            )
            message = f"Component is updated {self.info}"
            self.update_status(message)
            return resp
        except WeblateException as err:
            message = f"Component {self.info} can't be updated {err}"
            self.update_status(message)
            self.logger.error(f"{message}")
