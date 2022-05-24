
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from django.db import models


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(BaseRegisterForm, self).save()
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print('Custom group works!')
        return user

class User(models.Model):
    user = BaseRegisterForm.Meta.model.username
    print('username')


