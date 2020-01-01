from .models import Article, Category
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = ['title', 'created', 'category']
