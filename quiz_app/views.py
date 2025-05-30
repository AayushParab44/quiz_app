import json
import random
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import QuizUser, Question, QuizResult, QuizSession
from .forms import CustomUserCreationForm, QuizSelectionForm, QuizAnswerForm

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Quiz App!")

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure a QuizUser is created for the new user if not then create one
            QuizUser.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard_view(request):
    quiz_user = get_object_or_404(QuizUser, user=request.user)
    recent_results = QuizResult.objects.filter(user=quiz_user).order_by('-completed_at')[:5]
    return render(request, 'quiz_app/dashboard.html', {
        'quiz_user': quiz_user,
        'recent_results': recent_results
    })

@login_required
def quiz_selection_view(request):
    if request.method == 'POST':
        form = QuizSelectionForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            difficulty = form.cleaned_data['difficulty']
            
            # Get 10 random questions for the selected language and difficulty
            questions = list(Question.objects.filter(
                language=language,
                difficulty=difficulty
            ))
            
            if len(questions) < 10:
                messages.error(request, f'Not enough questions available for {language} - {difficulty}. Need at least 10 questions.')
                return render(request, 'quiz_app/quiz_selection.html', {'form': form})
            
            # Select 10 random questions
            selected_questions = random.sample(questions, 10)
            question_ids = [q.id for q in selected_questions]
            
            # Create quiz session
            quiz_user = get_object_or_404(QuizUser, user=request.user)
            session = QuizSession.objects.create(
                user=quiz_user,
                language=language,
                difficulty=difficulty,
                questions=json.dumps(question_ids)
            )
            
            return redirect('take_quiz', session_id=session.id)
    else:
        form = QuizSelectionForm()
    
    return render(request, 'quiz_app/quiz_selection.html', {'form': form})

@login_required
def take_quiz_view(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, user__user=request.user)
    question_ids = json.loads(session.questions)
    questions = Question.objects.filter(id__in=question_ids)
    
    if request.method == 'POST':
        form = QuizAnswerForm(questions, request.POST)
        if form.is_valid():
            # Calculate score
            score = 0
            results = []
            
            for question in questions:
                field_name = f'question_{question.id}'
                user_answer = form.cleaned_data.get(field_name)
                correct = False
                
                if question.question_type == 'boolean':
                    correct = bool(user_answer) == question.correct_boolean
                elif question.question_type == 'single_choice':
                    correct = user_answer == question.correct_answer
                elif question.question_type == 'multiple_choice':
                    if user_answer:
                        user_answer_set = set(user_answer)
                        correct_answer_set = set(question.correct_answer.split(','))
                        correct = user_answer_set == correct_answer_set
                elif question.question_type == 'text':
                    if user_answer and question.correct_answer:
                        correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                
                if correct:
                    score += 1
                
                results.append({
                    'question': question,
                    'user_answer': user_answer,
                    'correct': correct
                })
            
            # Calculate time taken
            time_taken = timezone.now() - session.start_time
            
            # Save result
            quiz_user = get_object_or_404(QuizUser, user=request.user)
            QuizResult.objects.create(
                user=quiz_user,
                language=session.language,
                difficulty=session.difficulty,
                score=score,
                total_time=time_taken
            )
            
            # Delete session
            session.delete()
            
            return render(request, 'quiz_app/quiz_result.html', {
                'score': score,
                'total': len(questions),
                'results': results,
                'time_taken': time_taken,
                'language': session.language,
                'difficulty': session.difficulty
            })
    else:
        form = QuizAnswerForm(questions)
    
    return render(request, 'quiz_app/take_quiz.html', {
        'form': form,
        'questions': questions,
        'session': session
    })

@login_required
def results_table_view(request):
    results = QuizResult.objects.all().order_by('-completed_at')
    return render(request, 'quiz_app/results_table.html', {'results': results})

@login_required
def results_data_view(request):
    results = QuizResult.objects.all().order_by('-completed_at')
    data = []
    for result in results:
        data.append({
            'id': result.id,
            'user_name': result.user.name,
            'language': result.language,
            'difficulty': result.difficulty,
            'score': f"{result.score}/10",
            'time_taken': result.get_time_display(),
            'completed_at': result.completed_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({'data': data})