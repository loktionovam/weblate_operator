from unittest import TestCase, mock
from weblate_operator.weblate.client import WeblateClient
from wlc import Weblate
import os


class TestWeblateClient(TestCase):
    def test_get_api_key_default(self):
        wc = WeblateClient()
        api_key = wc.get_api_key()
        self.assertEqual(api_key, "")

    @mock.patch.dict(
        os.environ, {"WEBLATE_API_KEY": "moomahx2oogheet7eiz5shu8oKukeeYeing8geije"}
    )
    def test_get_api_key_env(self):
        wc = WeblateClient()
        api_key = wc.get_api_key()
        self.assertEqual(api_key, "moomahx2oogheet7eiz5shu8oKukeeYeing8geije")

    def test_get_api_key_file(self):
        wc = WeblateClient(
            api_key_file_path="tests/apps/data/weblate-operator-secret/token"
        )
        api_key = wc.get_api_key()
        self.assertEqual(api_key, "wlu_HJfTnXjQ0uoiIve45hKpvCZFkpRDHxA8w13Y")

    def test_get_api_url_default(self):
        wc = WeblateClient()
        api_url = wc.get_api_url()
        self.assertEqual(api_url, "http://weblate/api/")

    @mock.patch.dict(os.environ, {"WEBLATE_API_URL": "http://weblate-api-url-env/api/"})
    def test_get_api_url_env(self):
        wc = WeblateClient()
        api_url = wc.get_api_url()
        self.assertEqual(api_url, "http://weblate-api-url-env/api/")

    def test_get_api_url_file(self):
        wc = WeblateClient(
            api_url_file_path="tests/apps/data/weblate-operator-config/api_url"
        )
        api_url = wc.get_api_url()
        self.assertEqual(api_url, "http://weblate-api-url-file/api/")

    def test_get_client(self):
        wc = WeblateClient()
        client = wc.get_client()
        self.assertIsInstance(client, Weblate)
