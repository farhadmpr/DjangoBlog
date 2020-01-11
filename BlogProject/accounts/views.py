from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm
from blog.models import Article

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login success',
                                 extra_tags='success')
                # return redirect('blog:index')
                return redirect(request.GET.get('next', 'blog:index'))
            else:
                messages.error(request, 'Login fail', extra_tags='danger')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                User.objects.get(username=cd['username'])
                messages.error(
                    request, 'The username has already been taken', extra_tags='danger')
                return redirect('accounts:user_register')
            except User.DoesNotExist:
                User.objects.create_user(
                    cd['username'],
                    cd['email'],
                    cd['password1'],
                )
                messages.success(request, 'Register success',
                                 extra_tags='success')
                return redirect('accounts:user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout success', 'success')
    return redirect('blog:index')


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    articles = Article.published.filter(writer=user)
    is_profile_owner = request.user.is_authenticated and request.user.id == user.id
    return render(request, 'accounts/profile.html',
                  {
                      'user': user,
                      'articles': articles,
                      'is_profile_owner': is_profile_owner
                  })


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            user.email = form.cleaned_data['email']
            user.save()
            messages.success(request, 'پروفایل با موفقیت ویرایش شد', 'success')
            return redirect('accounts:profile', user_id)
    else:
        form = EditProfileForm(instance=user.profile, initial={'email':user.email})
    return render(request, 'accounts/edit_profile.html', {'form': form})
