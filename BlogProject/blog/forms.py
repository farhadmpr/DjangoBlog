from django import forms
from .models import Article
from django.contrib.auth.models import User



class CommentForm(forms.Form):
    message = forms.CharField(max_length=500, label='Comment', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your comment',
        }
    ))


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'body', 'tags',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
