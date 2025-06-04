from django.contrib import admin
from .models import QuizUser, Question, Option, QuizResult, QuizSession

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

@admin.register(QuizUser)
class QuizUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'language', 'difficulty', 'question_type')
    list_filter = ('language', 'difficulty', 'question_type')
    search_fields = ('question_text',)
    inlines = [OptionInline]  # <-- Add this line

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'difficulty', 'score', 'total_time', 'completed_at')
    list_filter = ('language', 'difficulty', 'completed_at')
    search_fields = ('user__name',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'language', 'difficulty', 'start_time')
    list_filter = ('language', 'difficulty')




# from django.contrib import admin
# from .models import QuizUser, Question, QuizResult, QuizSession

# @admin.register(QuizUser)
# class QuizUserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'user', 'created_at')
#     search_fields = ('name', 'user__username')

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question_text', 'language', 'difficulty', 'question_type')
#     list_filter = ('language', 'difficulty', 'question_type')
#     search_fields = ('question_text',)

# @admin.register(QuizResult)
# class QuizResultAdmin(admin.ModelAdmin):
#     list_display = ('user', 'language', 'difficulty', 'score', 'total_time', 'completed_at')
#     list_filter = ('language', 'difficulty', 'completed_at')
#     search_fields = ('user__name',)

# @admin.register(QuizSession)
# class QuizSessionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'language', 'difficulty', 'start_time')
#     list_filter = ('language', 'difficulty')



# # admin.py
# from django.contrib import admin
# from .models import Question, Option

# class OptionInline(admin.TabularInline):
#     model = Option
#     extra = 4

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     inlines = [OptionInline]