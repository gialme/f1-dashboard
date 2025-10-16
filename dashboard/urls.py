from django.urls import path
from . import views

urlpatterns = [
    # homepage URL
    path('', views.homepage_view, name='homepage'),
    # last race data URL
    path('last-race/', views.last_race_view, name='last_race'),
]
