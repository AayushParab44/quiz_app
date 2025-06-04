from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class QuizUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Question(models.Model):
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('SQL', 'SQL'),
        ('C++', 'C++'),
    ]
    DIFFICULTY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    QUESTION_TYPES = [
        ('boolean', 'True/False'),
        ('single_choice', 'Single Choice (4 options)'),
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.TextField()
    correct_answer = models.TextField(null=True, blank=True)  # For text answers
    correct_boolean = models.BooleanField(null=True, blank=True)  # For boolean questions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.language} - {self.difficulty} - {self.question_text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200, blank=True)
    answer_seq = models.IntegerField(null=True, blank=True)  # Optional: for ordering
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer_text} ({'Correct' if self.is_correct else 'Incorrect'})"



class QuizResult(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)
    score = models.FloatField()
    total_time = models.DurationField()  # Time taken to complete quiz
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.language} ({self.difficulty}) - {self.score}/10"
    
    def get_time_display(self):
        total_seconds = int(self.total_time.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"

class QuizSession(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)
    start_time = models.DateTimeField(auto_now_add=True)
    questions = models.TextField()  # JSON string of question IDs
    
    def __str__(self):
        return f"{self.user.name} - {self.language} ({self.difficulty})"
    

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_quiz_user(sender, instance, created, **kwargs):
    if created:
        QuizUser.objects.get_or_create(user=instance, name=instance.username)




#Try to implement these-
# M2M (Many-to-Many)
# How it is defined?
# How to access?
# Through Table?


# class Question:
#     # Options for multiple choice questions


# class Option:
#     answer_text = models.CharField(max_length=200, blank=True)
#     answer_seq = models.IntegerField() # optional
#     question = models.Foreignkey(Question, related_name='answers')
#     is_correct = Foreignkey



# Question(id=1, question_text='WHat is Python?', opt1='Dynamic Programming Language', opt2='Not Object oriented')

# Option:
# Option(id=1, question=Question(id=1), answer_text='Dynamic Programming Language', is_correct=True)
# Option(id=2, question=Question(id=1), answer_text='Not Object oriented', is_correct=False)


# Approach 2:

# Question:
#     options = manytoMany()



# M2M -> Question_Options
