from wlc import Weblate
import os


class WeblateClient:
    def __init__(
        self,
        api_key_file_path="/var/run/secrets/weblate-operator-secret/token",
        api_url_file_path="/var/run/secrets/weblate-operator-config/api_url",
    ):
        self.api_key_file_path = api_key_file_path
        self.api_url_file_path = api_url_file_path
        self.api_key = self.get_api_key()
        self.api_url = self.get_api_url()
        self.weblate = Weblate(self.api_key, self.api_url, retries=1)

    def get_api_key(self):
        try:
            with open(self.api_key_file_path) as api_key_file:
                api_key = api_key_file.read().strip()
        except FileNotFoundError:
            api_key = os.environ.get("WEBLATE_API_KEY", "")
        return api_key

    def get_api_url(self):
        try:
            with open(self.api_url_file_path) as api_url_file:
                api_url = api_url_file.read().strip()
        except FileNotFoundError:
            api_url = os.environ.get("WEBLATE_API_URL", "http://weblate/api/")
        return api_url

    def get_client(self):
        return self.weblate
