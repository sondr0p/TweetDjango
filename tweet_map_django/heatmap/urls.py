from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='heatmap-home'),
    path('about/', views.about, name='heatmap-about'),
    path('search/', views.search, name='heatmap-search'),
]