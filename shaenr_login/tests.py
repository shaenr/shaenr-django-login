from django.test import TestCase

from .models import MyUser


# Create your tests here.
class MyUserTestCase(TestCase):
    def setUp(self) -> None:
        self.credentials = {
            'email': 'sdfdsfds@dsfsdds.com',
            'password': 'changethis!'
        }
        MyUser.objects.create_superuser(
            email=self.credentials['email'],
            email_verified=True,
            dob="1980-04-23",
            password=self.credentials['password']
        )

    def test_login(self):
        res = self.client.post('/admin/', self.credentials, follow=True)
        self.assertTrue(res.context['user'].is_active)