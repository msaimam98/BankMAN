from banks.models.banks import Bank

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.db import models 
import re



class BankForm(forms.ModelForm):
    description = forms.CharField(max_length=200, required=True)
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num', 'swift_code']
    