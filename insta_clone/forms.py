from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comments, Image, Profile, User


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['date_uploaded', 'user', 'likes']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
