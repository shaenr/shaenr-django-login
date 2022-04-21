import django.core.exceptions
from django.test import TestCase

from django.contrib.auth import get_user_model


class TestModelClass(TestCase):

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        """Run once to set up non-modified data for all class methods."""
        verified_email_dob_adult_superuser = cls.UserModel.objects.create(
            email="admin@admin.com",
            dob="1988-04-18",
            email_verified=True,
            is_superuser=True,
            is_staff=True
        )
        verified_email_dob_adult_user = cls.UserModel.objects.create(
            email="verified@internet.com",
            dob="1988-04-18",
            email_verified=True
        )
        unverified_email_dob_adult_user = cls.UserModel.objects.create(
            email="unverified@internet.com",
            dob="1988-04-18"
        )
        dob_not_adult_user = cls.UserModel.objects.create(
            email="child@internet.com",
            dob="2015-04-18"
        )
        defaults_only_email_given_user = cls.UserModel.objects.create(
            email="no_dob@internet.com")

    def setUp(self) -> None:
        """Run once for every test method to setup clean data."""
        pass

    def test_username_not_a_field_in_all_users(self):
        """There should be no username label"""
        all_users = self.UserModel.objects.all()
        for user in all_users:
            try:
                field_label = user._meta.get_field('username')
            except django.core.exceptions.FieldDoesNotExist as e:
                continue
            else:
                self.assertTrue(False)
            finally:
                self.assertTrue(True)
