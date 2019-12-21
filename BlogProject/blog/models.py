from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class PublishedArticlesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publish')


class Article(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish'),
    )

    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
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
