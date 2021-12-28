from datetime import timedelta

from django.test import TestCase

from .. import utils


class UtilsTestCase(TestCase):
    test_string = "abcdefgh"

    def test_is_dev_environment(self):
        with self.settings(ENVIRONMENT="dev"):
            self.assert_(utils.is_dev_environment())

    def test_is_dev_environment_false(self):
        with self.settings(ENVIRONMENT="prod"):
            self.assertFalse(utils.is_dev_environment())

    def test_get_token(self):
        encoded_string = utils.get_token(
            expires_in=timedelta(
                seconds=600),
            test_string=self.test_string)

        decoded_values = utils.decode_token(encoded_string)
        self.assertIsNotNone(decoded_values.get("exp"))
        self.assertEquals(self.test_string, decoded_values.get("test_string"))
