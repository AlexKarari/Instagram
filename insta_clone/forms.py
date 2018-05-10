from django import forms
from .models import Comments

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['poster', 'comment_time']

