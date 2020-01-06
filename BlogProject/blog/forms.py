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
    # Because I can't change ckeditor RichTextUploadingField with widget
    # I used this way to override it in textarea
    def __init__(self, *args, **kwargs):
        super(AddArticleForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = forms.Textarea(attrs={'class': 'form-control'})


    class Meta:
        model = Article
        fields = ('title', 'category', 'tags', 'body' )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title':'عنوان',
            'category':'دسته',
            'tags':'تگ',
            'body':'متن',
        }
    

class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'tags', 'body', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title':'عنوان',
            'category':'دسته',
            'tags':'تگ',
            'body':'متن',
        }        