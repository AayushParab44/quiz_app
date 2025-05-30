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
    
    # Options for multiple choice questions
    option_a = models.CharField(max_length=200, blank=True)
    option_b = models.CharField(max_length=200, blank=True)
    option_c = models.CharField(max_length=200, blank=True)
    option_d = models.CharField(max_length=200, blank=True)
    option_e = models.CharField(max_length=200, blank=True)
    
    # Correct answers
    correct_answer = models.TextField()  # For text answers or comma-separated for multiple choice
    correct_boolean = models.BooleanField(null=True, blank=True)  # For boolean questions
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.language} - {self.difficulty} - {self.question_text[:50]}"

class QuizResult(models.Model):
    user = models.ForeignKey(QuizUser, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10)
    score = models.IntegerField()
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