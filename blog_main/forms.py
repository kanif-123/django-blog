from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):  
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


# class LoginForm(AuthenticationForm):
#     class Meta:
#         model 