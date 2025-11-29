"""
URL configuration for recommendations app.
"""
from django.urls import path
from .views import get_recommendations, get_daily_picks

app_name = 'recommendations'

urlpatterns = [
    path('', get_recommendations, name='recommendations'),
    path('daily/', get_daily_picks, name='daily_picks'),
]
