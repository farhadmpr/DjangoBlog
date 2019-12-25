from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Comment
from .forms import CommentForm

# Create your views here.


def index(request):
    # articles = Article.objects.all().filter(status='publish')
    categories = Category.objects.all()

    search = request.GET.get('search')
    if search:
        lookups = Q(title__contains=search) | Q(body__contains=search)
        articles = Article.published.filter(
            lookups).distinct().order_by('-publish')
    else:
        articles = Article.published.all().order_by('-publish')

    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})


@login_required()
def details(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    comments = article.comments.all().order_by('created')
    article.view_count += 1
    article.save()

    if request.method == 'POST':
       form = CommentForm(request.POST) 
       if form.is_valid():
           message = form.cleaned_data['message']
           comment = Comment(message=message, writer=request.user, article=article)
           comment.save()
        
    return render(request, 'blog/details.html', {'article': article, 'comments': comments })


def categories(request, id):
    articles = Article.published.all().filter(category=id)
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})
