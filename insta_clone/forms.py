from django import forms
from .models import Comments, Image, Profile, User


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['date_uploaded', 'user', 'likes', 'profile']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
