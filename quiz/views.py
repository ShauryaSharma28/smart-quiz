# quiz/views.py  
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer

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


@login_required
def quiz_select(request):
    quizzes = Quiz.objects.all().order_by("title")
    return render(request, "quiz/quiz_select.html", {"quizzes": quizzes})

@login_required
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.create(
        user=request.user, quiz=quiz, started_at=timezone.now()
    )
    return redirect("quiz_take", attempt_id=attempt.id)

@login_required
def quiz_take(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    questions = attempt.quiz.questions.prefetch_related("answers")
    return render(request, "quiz/quiz_take.html", {"attempt": attempt, "questions": questions})

@login_required
def quiz_submit(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    questions = attempt.quiz.questions.all()

    # Optional server-side enforcement
    if attempt.started_at and attempt.duration_seconds:
        elapsed = (timezone.now() - attempt.started_at).total_seconds()
        if elapsed > attempt.duration_seconds + 5:  # small grace period
            return redirect("attempt_detail", attempt_id=attempt.id)

    # Grade and store user answers
    total_correct = 0
    for q in questions:
        selected_id = request.POST.get(f"q_{q.id}")
        if not selected_id:
            continue
        selected = Answer.objects.filter(id=selected_id, question=q).first()
        if not selected:
            continue
        UserAnswer.objects.create(
            quiz_attempt=attempt, question=q, selected_answer=selected
        )
        if selected.is_correct:
            total_correct += 1

    attempt.score = total_correct
    attempt.date_completed = timezone.now()
    attempt.save()
    return redirect("attempt_detail", attempt_id=attempt.id)