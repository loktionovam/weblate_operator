from unittest import TestCase
from time import time
from unittest import TestCase
from webbrowser import get
import responses

try:
    from tests.apps.misc.weblate_data import *
except ImportError:
    from misc.weblate_data import *


class TestWeblate(TestCase):
    def setUp(self):
        super().setUp()
        responses.mock.start()
        responses.add(
            responses.GET,
            API_URL + "projects/test-project/",
            json=PROJECT_RESPONSE,
            status=200,
        )

        responses.add(
            responses.POST, f"{API_URL}projects/", json=PROJECT_RESPONSE, status=201
        )

        responses.add(
            responses.DELETE, f"{API_URL}projects/{PROJECT_NAME}/", status=200
        )

        responses.add(
            responses.PATCH,
            f"{API_URL}projects/{PROJECT_NAME}/",
            json=PROJECT_RESPONSE,
            status=200,
        )

        responses.add(
            responses.POST,
            f"{API_URL}projects/{PROJECT_NAME}/components/",
            json=COMPONENT_RESPONSE,
            status=201,
        )

        responses.add(
            responses.GET,
            f"{API_URL}components/{PROJECT_NAME}/{COMPONENT_NAME}/",
            json=COMPONENT_RESPONSE,
            status=200,
        )

        responses.add(
            responses.PATCH,
            f"{API_URL}components/{PROJECT_NAME}/{COMPONENT_NAME}/",
            json=COMPONENT_RESPONSE,
            status=200,
        )

        responses.add(
            responses.DELETE,
            f"{API_URL}components/{PROJECT_NAME}/{COMPONENT_NAME}/",
            status=200,
        )

        responses.add(
            responses.GET,
            f"{API_URL}translations/{PROJECT_NAME}/{COMPONENT_NAME}/{TRANSLATION_NAME}/",
            json=TRANSLATION_RESPONSE,
            status=200,
        )

        responses.add(
            responses.DELETE,
            f"{API_URL}translations/{PROJECT_NAME}/{COMPONENT_NAME}/{TRANSLATION_NAME}/",
            status=200,
        )

        responses.add(
            responses.POST,
            f"{API_URL}components/{PROJECT_NAME}/{COMPONENT_NAME}/translations/",
            json=TRANSLATION_RESPONSE,
            status=201,
        )

    def tearDown(self):
        """Disable responses."""
        responses.mock.stop()
        responses.mock.reset()
