from . import client as wc
from . import WeblateAbstract
from wlc import WeblateException
import kubernetes


class WeblateProject(WeblateAbstract):
    def __init__(self, namespace, body, logger):
        super().__init__(namespace, "weblateprojects", body)
        self.name = self.spec["weblateProjectConfiguration"]["name"]
        self.slug = self.spec["weblateProjectConfiguration"]["slug"]
        self.web = self.spec["weblateProjectConfiguration"]["web"]
        self.info = f"name: {self.name}, slug: {self.slug}, web: {self.web}"
        self.logger = logger
        self.api_path = f"projects/{self.slug}/"

    def delete(self):

        retention_policy = self.spec["weblateProjectRetentionPolicy"]["whenDeleted"]
        self.logger.info(f"Weblate project retention policy: {retention_policy}")

        if retention_policy == "Delete":

            try:
                weblate_project = self.weblate.get_project(path=self.slug)
                resp = weblate_project.delete()
                self.logger.info(f"Project is deleted {self.info}")
                return resp
            except Exception as err:
                self.logger.error(err)

    def create(self):
        try:
            resp = self.weblate.create_project(self.name, self.slug, self.web)
            message = f"Project is created {self.info}"
            self.update_status(message)
            return resp
        except WeblateException as err:
            error_msg = str(err)
            if "HTTP error 400" in error_msg and "already exist" in error_msg:
                return self.update()
            else:
                raise err

    def update(self):
        try:
            resp = self.weblate.request(
                "patch",
                path=self.api_path,
                data={"name": self.name, "web": self.web},
            )
            message = f"Project is updated {self.info}"
            self.update_status(message)
            self.logger.info(message)
            return resp
        except WeblateException as err:
            message = f"Project {self.info} can't be updated {err}"
            self.update_status(message)
            self.logger.error(f"{message}")
