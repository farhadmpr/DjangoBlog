from django import forms
from django.contrib.auth.models import User


class CommentForm(forms.Form):
    message = forms.CharField(max_length=500, label='Comment', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your comment',
        }
    ))       