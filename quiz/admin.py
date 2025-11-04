from django.contrib import admin
from .models import Quiz, Question, Answer, QuizAttempt, UserAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('text', 'is_correct')
    readonly_fields = ()
    show_change_link = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "question_text")
    inlines = [AnswerInline]


admin.site.register(Quiz)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)
# IMPORTANT: Do not also call admin.site.register(Question) anywhere else.
