from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import QuizUser, Question

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class QuizSelectionForm(forms.Form):
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
    
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class QuizAnswerForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in questions:
            field_name = f'question_{question.id}'
            if question.question_type == 'boolean':
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('True', 'True'), ('False', 'False')],
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False
                )
            elif question.question_type == 'single_choice':
                # Use Option model for choices
                choices = [(str(opt.id), opt.answer_text) for opt in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False
                )
            elif question.question_type == 'multiple_choice':
                choices = [(str(opt.id), opt.answer_text) for opt in question.options.all()]
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices,
                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                    required=False
                )
            elif question.question_type == 'text':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    required=False
                )


