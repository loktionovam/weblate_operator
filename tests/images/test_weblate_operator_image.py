import subprocess
from unittest import TestCase
import pytest
import json
from time import sleep


@pytest.mark.usefixtures("host")
class TestRequirements(TestCase):
    """
    Check the requirements for running the bot are set up in the Docker image
    correctly
    """

    def setUp(self):
        super(TestRequirements, self).setUp()

    def test_weblate_operator_process(self):
        """
        Check that exactly one python process launched
        and it is non-root process
        """

        process = self.host.process.get(comm="kopf")
        self.assertEqual("weblate_", process.user, msg={process.user})
        self.assertEqual("nogroup", process.group, msg={process.group})

    def test_weblate_operator_logs(self):
        """
        Test that weblate operator writes logs in json format
        """
        sleep(5)
        log_entry = (
            subprocess.check_output(
                ["docker", "logs", self.host.backend.name], stderr=subprocess.STDOUT
            )
            .decode()
            .split("\n")[0]
        )
        parsed_log_entry = json.loads(log_entry)
        self.assertEqual("info", parsed_log_entry["severity"], msg=parsed_log_entry)
