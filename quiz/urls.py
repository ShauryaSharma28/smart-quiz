from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard/<int:quiz_id>/', views.leaderboard, name='leaderboard'),
    path('history/', views.history, name='history'),
    path('attempt/<int:attempt_id>/', views.attempt_detail, name='attempt_detail'),
]
