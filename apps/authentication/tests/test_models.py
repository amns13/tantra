from datetime import timedelta
from typing import Optional

from django.db.utils import IntegrityError
from django.test import TestCase

from ...core.utils import decode_token, get_token
from .. import constants
from ..models import User


class UserTestCase(TestCase):
    """test User model"""
    existing_username = "existing_username"
    existing_email = "existing_email"
    default_password = "password"

    @classmethod
    def setUpTestData(cls):
        cls.existing_user = User.objects.create(
            username=cls.existing_username,
            email=cls.existing_email,
            password=cls.default_password)

    def setUp(self):
        self.test_email = "testemail@example.com"
        self.test_username = "testusername"

    def create_test_user(self, username: Optional[str] = None, email: Optional[str]
                         = None, password: Optional[str] = None, superuser: bool = False) -> User:
        if not username:
            username = self.test_username

        if not email:
            email = self.test_email

        if not password:
            password = self.default_password

        create_user_func = User.objects.create_user
        if superuser:
            create_user_func = User.objects.create_superuser

        return create_user_func(
            username=username, email=email, password=password)

    def test_creatpe_user_with_correct_input(self):
        user = self.create_test_user()

        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(str(user), self.test_username)

    def test_create_superuser_with_correct_input(self):
        user = self.create_test_user(superuser=True)

        self.assert_(user.is_verified)
        self.assert_(user.is_superuser)
        self.assert_(user.is_staff)

    def test_dupliccate_username(self):
        self.assertRaises(
            IntegrityError,
            self.create_test_user,
            username=self.existing_username)

    def test_duplicate_email(self):
        self.assertRaises(
            IntegrityError,
            self.create_test_user,
            email=self.existing_email)

    def test_null_username(self):
        self.assertRaises(
            TypeError,
            User.objects.create_user,
            username=None,
            email=self.test_email,
            password=self.default_password)

    def test_null_email(self):
        self.assertRaises(
            TypeError,
            User.objects.create_user,
            username=self.test_username,
            email=None,
            password=self.default_password)

    def test_null_password(self):
        self.assertRaises(
            TypeError,
            User.objects.create_user,
            username=self.test_username,
            email=self.test_email,
            password=None)

    def test_verify_account(self):
        user = self.create_test_user()
        user.verify_account()
        self.assert_(user.is_verified)

    def test_get_email_verification_token(self):
        user = self.existing_user
        token = user.get_email_verification_token()

        decoded_values = decode_token(token)
        self.assertIsNotNone(decoded_values.get("exp"))
        self.assertEquals(str(user.uuid), decoded_values.get("verify_email"))

    def test_get_password_rest_token(self):
        user = self.existing_user
        token = user.get_password_reset_token()

        decoded_values = decode_token(token)
        self.assertIsNotNone(decoded_values.get("exp"))
        self.assertEquals(str(user.uuid), decoded_values.get("reset_password"))

    def test_verify_email_verification_token(self):
        user = self.existing_user
        token = user.get_email_verification_token()
        user_from_token = User.verify_email_verification_token(token)
        self.assertIsNotNone(user_from_token)
        self.assertEquals(user.pk, user_from_token.pk)

    def test_verify_password_reset_token(self):
        user = self.existing_user
        token = user.get_password_reset_token()
        user_from_token = User.verify_password_reset_token(token)
        self.assertIsNotNone(user_from_token)
        self.assertEquals(user.pk, user_from_token.pk)

    def test_verify_email_verification_token_for_wrong_user(self):
        token = get_token(
            expires_in=timedelta(
                seconds=600),
            test_string="test_string")
        user_from_token = User.verify_email_verification_token(token)
        self.assertIsNone(user_from_token)

    def test_verify_password_reset_token_for_wrong_user(self):
        token = get_token(
            expires_in=timedelta(
                seconds=600),
            test_string="test_string")
        user_from_token = User.verify_password_reset_token(token)
        self.assertIsNone(user_from_token)
