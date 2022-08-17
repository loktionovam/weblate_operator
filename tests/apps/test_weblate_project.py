from unittest import mock
from time import time
import unittest
from webbrowser import get
from tests.apps.misc.utils import KubernetesManifestRunner
from kopf.testing import KopfRunner
import os
import time
from tests.apps.misc.weblate_data import API_URL
from test_weblate import TestWeblate


class TestWeblateProject(TestWeblate):
    def setUp(self):
        super().setUp()
        self.project_crd = KubernetesManifestRunner("crds/crd-weblateproject.yaml")
        self.project_crd.create()

    @mock.patch.dict(
        os.environ,
        {
            "WEBLATE_API_URL": API_URL,
        },
    )
    def test_project(self):

        with KopfRunner(
            ["run", "-A", "--verbose", "weblate_operator/operator.py"]
        ) as runner:
            self.project = KubernetesManifestRunner("tests/apps/data/test-project.yaml")
            self.project.create()
            time.sleep(2)

            patch = {
                "spec": {
                    "weblateProjectConfiguration": {"name": "test-project-patched"}
                }
            }
            self.project.patch(patch)
            time.sleep(2)

            self.project.delete()
            time.sleep(2)
        assert runner.exit_code == 0
        assert runner.exception is None
        assert (
            "Project is created name: test-project, slug: test-project" in runner.stdout
        )
        assert (
            "Project is updated name: test-project-patched, slug: test-project"
            in runner.stdout
        )
        assert (
            "Project is deleted name: test-project-patched, slug: test-project"
            in runner.stdout
        )

    def tearDown(self):
        super().tearDown()
        self.project_crd.delete()


if __name__ == "__main__":
    unittest.main()
