from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomUserModelBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, request, **kwargs):
        email = kwargs['email']
        password = kwargs['password']

        if email is None:
            email = kwargs.get(
                "email",
                kwargs.get(UserModel.EMAIL_FIELD)
            )

        if email is None or password is None:
            return

        try:
            # Test this
            user = UserModel._default_manager.get(
                Q(email__exact=email) | (Q(email__iexact=email) & Q(email_verified=True))
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        """
        Reject users without email verified.
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        if user.email_verified:
            is_active = getattr(user, "is_active", None)
        else:
            is_active = False
        return is_active or is_active is None


