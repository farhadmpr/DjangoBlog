from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article

# Create your views here.


def index(request):
    # articles = Article.objects.all().filter(status='publish')
    articles = Article.published.all()
    return render(request, 'blog/index.html', {'articles': articles})

@login_required()
def details(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    return render(request, 'blog/details.html', {'article': article})
