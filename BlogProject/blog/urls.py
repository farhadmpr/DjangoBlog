from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:id>/', views.categories, name='categories'),
    # path('details/<int:id>/<slug:slug>/', views.details, name='details'),
    # https://stackoverflow.com/questions/55175353/django-slug-url-in-perisan-404
    re_path('details/(?P<id>[0-9]+)/(?P<slug>[\\w-]+)/', views.details, name='details'),
    path('add_article/', views.add_article, name='add_article'),
]