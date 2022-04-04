from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from polls.models import UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

class UserProfileForm(ModelForm):
    class Meta:
        fi = [f.name for f in User._meta.get_fields()]
        model = UserProfile
        fields = ["phone"]
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

userProfileFormSet = inlineformset_factory(User, UserProfile, form=UserProfileForm, extra=2)