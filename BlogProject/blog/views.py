from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Comment, Tag
from .forms import CommentForm, AddArticleForm
from django.utils.text import slugify
from django.contrib import messages

from rest_framework import viewsets
from .serializers import ArticleSerializer

# Create your views here.


def index(request):
    # articles = Article.objects.all().filter(status='publish')
    categories = Category.objects.all()

    search = request.GET.get('search')
    tag_id = request.GET.get('tag')

    if tag_id:
        #tag = Tag.objects.get(id=tag_id)
        tag = Tag.objects.filter(id=tag_id).first()
        if tag:
            articles = tag.article_set.filter(status='publish').all()
        else:
            articles = None
    elif search:
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
            comment = Comment(
                message=message, writer=request.user, article=article)
            comment.save()

    return render(request, 'blog/details.html', {'article': article, 'comments': comments})


def categories(request, id):
    articles = Article.published.all().filter(category=id)
    categories = Category.objects.all()
    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.writer = request.user
            article.slug = slugify(form.cleaned_data['title'][:30], allow_unicode=True)
            tags = form.cleaned_data['tags']
            article.save()   
            article.tags.add(*tags)            
            messages.success(request, 'نوشته با موفقیت ذخیره شد', 'success')
            return redirect('accounts:profile', request.user.id)
    else:
        form = AddArticleForm()
    return render(request, 'blog/add_article.html', {'form': form})


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()  # .order_by('-created')
    serializer_class = ArticleSerializer
