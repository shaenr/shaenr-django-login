from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomUserModelBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        try:
            user = UserModel._default_manager.get(
                Q(email__iexact=username) | Q(email__iexact=email)
            )
        except UserModel.DoesNotExist:
            print("User does not exist")
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            print("Multiple returned")
            user = UserModel.objects.filter(
                Q(email__iexact=email)
            ).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user


