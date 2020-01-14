from django.db.models import Q, Count, Subquery, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Comment, Tag, Vote
from .forms import CommentForm, AddArticleForm, EditArticleForm
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

    # همه دسته ها به اضافه عنوان مقاله داخل آن دسته که بیشترین تعداد تگ را داشته باشد
    article_subquery = Article.objects.filter(category=OuterRef('pk')).annotate(
        tags_count=Count('tags')).order_by('-tags_count')
    cats_articles = Category.objects.annotate(
        best_article=Subquery(article_subquery.values('title')[:1]))
    ####

    return render(request, 'blog/index.html', {'articles': articles, 'categories': categories})


@login_required()
def details(request, id, slug):
    article = get_object_or_404(Article, id=id, slug=slug)
    comments = article.comments.all().order_by('created')
    article.view_count += 1
    article.save()

    can_like = article.user_can_like(request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            comment = Comment(
                message=message, writer=request.user, article=article)
            comment.save()

    return render(request, 'blog/details.html', {'article': article, 'comments': comments, 'can_like': can_like})


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
            article.slug = slugify(
                form.cleaned_data['title'][:30], allow_unicode=True)
            tags = form.cleaned_data['tags']
            article.save()
            article.tags.add(*tags)
            messages.success(
                request, 'نوشته با موفقیت ذخیره شد و بعد از تایید مدیر نمایش داده خواهد شد', 'success')
            return redirect('accounts:profile', request.user.id)
    else:
        form = AddArticleForm()
    return render(request, 'blog/add_article.html', {'form': form})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user.id == article.writer.id:
        if request.method == 'POST':
            form = EditArticleForm(request.POST, instance=article)
            if form.is_valid():
                article = form.save(commit=False)
                article.slug = slugify(
                    form.cleaned_data['title'][:30], allow_unicode=True)
                tags = form.cleaned_data['tags']
                article.tags.clear()
                article.save()
                article.tags.add(*tags)
                messages.success(
                    request, 'نوشته با موفقیت ویرایش شد', 'success')
                return redirect('accounts:profile', request.user.id)
        else:
            form = EditArticleForm(instance=article)
        return render(request, 'blog/edit_article.html', {'form': form})
    return redirect('accounts:profile', request.user.id)


@login_required
def delete_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.user.id == article.writer.id:
        article.delete()
        messages.success(request, 'با موفقیت حذف شد', 'danger')
    return redirect('accounts:profile', request.user.id)


@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.user_can_like(request.user):
        vote = Vote(article=article, user=request.user)
        vote.save()
        messages.success(request, 'لایک ثبت شد', 'success')
    else:
        article.vote_set.filter(user=request.user).delete()
        messages.error(request, 'لایک حذف شد', 'danger')

    return redirect('blog:details', article.id, article.slug)

# rest framework


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()  # .order_by('-created')
    serializer_class = ArticleSerializer
