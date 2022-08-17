from unittest import TestCase, mock
from time import time
from unittest import TestCase
import unittest
from webbrowser import get
import responses

try:
    from tests.apps.misc.utils import KubernetesManifestRunner
except ImportError:
    from misc.utils import KubernetesManifestRunner
from kopf.testing import KopfRunner
import os
import time

try:
    from tests.apps.misc.weblate_data import API_URL
except ImportError:
    from misc.weblate_data import API_URL
from test_weblate import TestWeblate


class TestWeblateProject(TestWeblate):
    def setUp(self):
        super().setUp()
        self.project_crd = KubernetesManifestRunner("crds/crd-weblateproject.yaml")
        self.project_crd.create()

        self.component_crd = KubernetesManifestRunner("crds/crd-weblatecomponent.yaml")
        self.component_crd.create()

    @mock.patch.dict(
        os.environ,
        {
            "WEBLATE_API_URL": API_URL,
        },
    )
    def test_component(self):

        with KopfRunner(
            ["run", "-A", "--verbose", "weblate_operator/operator.py"]
        ) as runner:
            self.project = KubernetesManifestRunner("tests/apps/data/test-project.yaml")
            self.project.create()
            time.sleep(2)

            self.component = KubernetesManifestRunner(
                "tests/apps/data/test-component.yaml"
            )
            self.component.create()
            time.sleep(2)

            patch = {
                "spec": {
                    "weblateComponentConfiguration": {"name": "test-component-patched"}
                }
            }
            self.component.patch(patch)
            time.sleep(2)

            self.component.delete()
            time.sleep(2)

            self.project.delete()
            time.sleep(2)
        assert runner.exit_code == 0
        assert runner.exception is None
        assert (
            "Component is created name: test-component, slug: test-component, project_slug: test-project"
            in runner.stdout
        )
        assert (
            "Component is updated name: test-component-patched, slug: test-component, project_slug: test-project"
            in runner.stdout
        )
        assert (
            "Component is deleted name: test-component-patched, slug: test-component, project_slug: test-project"
            in runner.stdout
        )

    def tearDown(self):
        """Disable responses."""
        responses.mock.stop()
        responses.mock.reset()

        self.component_crd.delete()
        self.project_crd.delete()


if __name__ == "__main__":
    unittest.main()
