from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root of /quiz/
    path('leaderboard/<int:quiz_id>/', views.leaderboard, name='leaderboard'),
]
