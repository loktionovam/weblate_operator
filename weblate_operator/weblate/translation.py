from . import WeblateAbstract
from wlc import WeblateException


class WeblateTranslation(WeblateAbstract):
    def __init__(self, namespace, body, logger):
        super().__init__(namespace, "weblatetranslations", body)
        self.project_slug = self.spec["weblateTranslationConfiguration"]["projectSlug"]
        self.component_slug = self.spec["weblateTranslationConfiguration"][
            "componentSlug"
        ]
        self.language_code = self.spec["weblateTranslationConfiguration"][
            "languageCode"
        ]
        self.info = f"language code: {self.language_code}, project slug: {self.project_slug}, component slug: {self.component_slug}"
        self.logger = logger
        self.component_path = f"{self.project_slug}/{self.component_slug}"
        self.translation_path = f"{self.component_path}/{self.language_code}"
        self.api_path = f"translations/{self.translation_path}/"

    def create(self):
        try:
            component = self.weblate.get_component(path=f"{self.component_path}")
            resp = component.add_translation(self.language_code)
            message = f"Translation is created {self.info}"
            self.logger.info(message)
            self.update_status(message)
            return resp
        except WeblateException as err:
            error_msg = str(err)
            if "HTTP error 400" in error_msg and "already exist" in error_msg:
                pass
            else:
                raise err

    def delete(self):
        retention_policy = self.spec["weblateTranslationRetentionPolicy"]["whenDeleted"]
        self.logger.info(f"Weblate translation retention policy: {retention_policy}")

        if retention_policy == "Delete":

            try:
                weblate_translation = self.weblate.get_translation(
                    path=self.translation_path
                )
                resp = weblate_translation.delete()
                self.logger.info(f"Translation is deleted {self.info}")
                return resp
            except Exception as err:
                self.logger.error(err)

    def update(self):
        raise NotImplementedError
