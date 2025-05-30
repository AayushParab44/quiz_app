from django.contrib import admin
from .models import QuizUser, Question, QuizResult, QuizSession

@admin.register(QuizUser)
class QuizUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'language', 'difficulty', 'question_type')
    list_filter = ('language', 'difficulty', 'question_type')
    search_fields = ('question_text',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'difficulty', 'score', 'total_time', 'completed_at')
    list_filter = ('language', 'difficulty', 'completed_at')
    search_fields = ('user__name',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'difficulty', 'start_time')
    list_filter = ('language', 'difficulty')