from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Category

# Create your views here.


def index(request):
    # articles = Article.objects.all().filter(status='publish')
    articles = Article.published.all()
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})


def categories(request, id):
    articles = Article.published.all().filter(category=id)
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})


@login_required()
def details(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    return render(request, 'blog/details.html', {'article': article})
