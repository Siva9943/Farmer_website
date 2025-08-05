from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from allauth.socialaccount.forms import SignupForm
from allauth.account.forms import LoginForm
from django.contrib.auth.models import User

class CustomUserForm(UserCreationForm):
    username=forms.CharField()
    email=forms.CharField()
    password1=forms.CharField()
    password2=forms.CharField()
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class MyCustomSocialSignupForm(SignupForm):
    def save(self, request):
        print(request,"gfgfg")
        user = super().save(request)
        return user
class MyCustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        print("gfgfgggggggg")
        return super().login(*args, **kwargs)
    


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')
