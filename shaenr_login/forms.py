from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import MyUser


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = MyUser
        fields = ('email', 'dob')
