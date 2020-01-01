from django import forms
from django.contrib.auth.models import User


errors = {
    'required': 'این فیلد را حتما وارد کنید',
    'max_length': 'تعداد حروف بیش از حد است',
}

class UserLoginForm(forms.Form):    
    username = forms.CharField(max_length=30, error_messages=errors, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your username',
        }
    ))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your password',
        }))

###############################################################################


class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your email',
        }
    ))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter your email',
        }
    ))
    password1 = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={            
            'class': 'form-control',
            'placeholder': 'enter your password',
        }))
    password2 = forms.CharField(label='Confirm Password', max_length=50, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'confirm your password',
        }))

    # field level
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('This email already exists')
        return email

    # def clean_password2(self):
    #     p1 = self.cleaned_data['password1']
    #     p2 = self.cleaned_data['password2']
    #     if p1 != p2:
    #         raise forms.ValidationError('passwords not same')        
    #     return p1

    # form level
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('passwords not same')


         