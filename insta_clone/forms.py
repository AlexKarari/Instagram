from django import forms
from .models import Comments, Image


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['poster', 'comment_time']


class NewStatusForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['image_name', 'profile', 'likes']
        
