from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:id>/<slug:slug>/', views.details, name='details'),

]