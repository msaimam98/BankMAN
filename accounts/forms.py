from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.db import models 
import re



# LOG IN FORM 
class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError({
                'username' : 'Username or password is invalid'}
            )
        data['user'] = user
        return data



# SIGN UP FORM
def exists_username(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


class SignupForm(UserCreationForm):  
    
    # required false so that I can override the input tags frontend error checking 
    # username = forms.CharField(max_length=120, required=False)

    # password1 = forms.CharField(
    #     label="Password",
    #     widget=forms.PasswordInput(),
        
    # )

    # password2 = forms.CharField(
    #     label="Password confirmation",
    #     widget=forms.PasswordInput(),
    #     help_text="Enter the same password as before, for verification.",
       
    # )
    # dont have strip-False -> doesnt strip the field we specified that for 

    # required false so that I can override the input tags frontend error checking 
    # email = forms.EmailField(required=False)
    # first_name = forms.CharField(max_length=120, required=False)
    # last_name = forms.CharField(max_length=120, required=False)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

        # model = User

        # need emailField so backend knows this is an email field, to protect from someone trying to pass malicious data in the email field
        # fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']



    # def clean(self):

    #     # this is where we do the error adding 

    #     # get the data 
    #     data = super().clean()


    #     # check if username is an empty string 
    #     if 'username' in data:
    #         if data['username'] == '':
    #             self.add_error('username', 'This field is required')
    #             # once this error is added from the username field, the username field is removed hence the else if 
    #         else:
    #             if exists_username(data['username']):
    #                 self.add_error('username', 'A user with that username already exists')

    #     # check if password is not inputed, if not, send an error 
    #     if data['password1'] == '':
    #         self.add_error('password1', 'This field is required')


        # email validator
        # email = data['email']
        # regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        # if email == '':
        #     self.add_error('email', 'Enter a valid email address')
        # elif not re.fullmatch(regex, email):
        #     self.add_error('email', 'Enter a valid email address')
        # note: common password validator is in action, but its fine - the autotester doesnt check for that 

        

        # return data
    
















# PROFILE FORM


class EditProfileForm(forms.ModelForm):

    # inherits from SignUpForm therefore it has all error checking and all fields 

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(),
        help_text="Enter the same password as before, for verification.",
        required=False,
    )

    # # required false so that I can override the input tags frontend error checking 
    # email = forms.EmailField(required=False)
    # first_name = forms.CharField(max_length=120, required=False)
    # last_name = forms.CharField(max_length=120, required=False)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


    def clean(self):

        data = super().clean()
        print("is there password in here?",data)

        # if password1 not in the data that was cleaned, that means either there was an error OR nothing was submitted for the password
        if 'password1' in data:
            if data['password1'] != data['password2']:
                self.add_error('password1', "The two password fields didn't match")
            elif len(data['password1']) < 8 and len(data['password1']) > 0:
                self.add_error('password1', "This password is too short. It must contain at least 8 characters")
        
        

        return data

    # def clean(self):

    #     # this is where we do the error adding 

    #     # get the data 
    #     data = super().clean()
    #     print(data, 'this is the data')

    #     # check if password is not inputed, that means the user does not want to change their password 
    #     if data['password1'] == '':
    #         pass

    #     print(data, 'after the password is checked')


    #     # email validator
    #     email = data['email']
    #     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    #     if email == '':
    #         self.add_error('email', 'Enter a valid email address')
    #     elif not re.fullmatch(regex, email):
    #         self.add_error('email', 'Enter a valid email address')
    #     # note: common password validator is in action, but its fine - the autotester doesnt check for that 

        

    #     return data

        

    

    

    

