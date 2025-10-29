from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import QuizAttempt, UserAnswer, Answer

@login_required
def home(request):
    latest_attempt = QuizAttempt.objects.filter(user=request.user).order_by('-date_completed').first()
    return render(request, 'quiz/home.html', {'latest_attempt': latest_attempt})


def leaderboard(request, quiz_id):
    top_attempts = QuizAttempt.objects.filter(quiz_id=quiz_id).order_by('-score')[:10]
    return render(request, 'quiz/leaderboard.html', {'top_attempts': top_attempts})

@login_required
def history(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-date_completed')
    return render(request, 'quiz/history.html', {'attempts': attempts})

@login_required
def attempt_detail(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(quiz_attempt=attempt)

    qa_details = []
    for ua in user_answers:
        q = ua.question
        answers = Answer.objects.filter(question=q)
        qa_details.append({
            'question': q,
            'answers': answers,
            'selected_answer_id': ua.selected_answer.id,
        })

    context = {
        'attempt': attempt,
        'qa_details': qa_details,
    }
    return render(request, 'quiz/attempt_detail.html', context)
