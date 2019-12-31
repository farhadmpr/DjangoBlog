from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# Create your models here.


class PublishedArticlesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publish')


class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    view_count = models.IntegerField(default=0, editable=False)
    # body = models.TextField()
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    objects = models.Manager()
    published = PublishedArticlesManager()

    def get_absolute_url(self):
        return reverse('blog:details', args=[self.id, self.slug])
        #return reverse('blog:details', args=[self.id, slugify(self.slug, allow_unicode=True) ])


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.message[:100]
