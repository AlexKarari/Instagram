from django import forms
from .models import Comments, Post

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user', 'post']


class NewStatusForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'profile', 'date_posted', 'tags']
        
