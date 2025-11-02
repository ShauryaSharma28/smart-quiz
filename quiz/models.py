# quiz/models.py

from django.db import models
from django.contrib.auth.models import User

# Model for the Quiz Category
class Quiz(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title

# Model for the individual Question
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    
    def __str__(self):
        return self.question_text[:50] 

# Model for the Answer Choices
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=255)   # this field must exist
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# Model to track user attempts and scores
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    score = models.IntegerField(default=0)
    date_completed = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)        # optional timing
    duration_seconds = models.IntegerField(default=600)              # 10 minutes default
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score})"
    
class UserAnswer(models.Model):
    quiz_attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz_attempt.user.username} - Q: {self.question.id} - A: {self.selected_answer.id}"
