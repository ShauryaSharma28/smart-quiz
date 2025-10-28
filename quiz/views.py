from django.shortcuts import render
from .models import QuizAttempt

def home(request):
    return render(request, 'quiz/home.html')


def leaderboard(request, quiz_id):
    top_attempts = QuizAttempt.objects.filter(quiz_id=quiz_id).order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'top_attempts': top_attempts})
