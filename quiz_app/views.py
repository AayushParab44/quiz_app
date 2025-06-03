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
            # REMOVE this line:
            # QuizUser.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Ensure a QuizUser is created for the new user if not then create one
#             QuizUser.objects.get_or_create(user=user)
#             login(request, user)
#             messages.success(request, 'Registration successful!')
#             return redirect('dashboard')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})

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
            
            if len(questions) < 1:
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

# @login_required
# def take_quiz_view(request, session_id):
#     session = get_object_or_404(QuizSession, id=session_id, user__user=request.user)
#     question_ids = json.loads(session.questions)
#     questions = Question.objects.filter(id__in=question_ids)
    
#     if request.method == 'POST':
#         form = QuizAnswerForm(questions, request.POST)
#         if form.is_valid():
#             # Calculate score
#             score = 0
#             results = []
            
#             for question in questions:
#                 field_name = f'question_{question.id}'
#                 user_answer = form.cleaned_data.get(field_name)
#                 correct = False
                
#                 if question.question_type == 'boolean':
#                     if user_answer is not None and user_answer != '':
#                         correct = (user_answer == str(question.correct_boolean))
#                     else:
#                         correct = False
#                 elif question.question_type == 'single_choice':
#                     correct = user_answer == question.correct_answer
#                 elif question.question_type == 'multiple_choice':
#                     if user_answer:
#                         # Always treat as a set of strings
#                         if isinstance(user_answer, str):
#                             user_answer_set = set([user_answer])
#                         else:
#                             user_answer_set = set(user_answer)
#                         correct_answer_set = set(ans.strip() for ans in question.correct_answer.split(',') if ans.strip())
#                         # Only correct if all and only the correct options are selected
#                         correct = user_answer_set == correct_answer_set
#                     else:
#                         correct = False

                        
#                         # user_answer_set = set(user_answer)
#                         # correct_answer_set = set(question.correct_answer.split(','))
#                         # correct = user_answer_set == correct_answer_set
#                 elif question.question_type == 'text':
#                     if user_answer and question.correct_answer:
#                         correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                
#                 if correct:
#                     score += 1
                
#                 # results.append({
#                 #     'question': question,
#                 #     'user_answer': user_answer,
#                 #     'correct': correct
#                 # })
#                 results.append({
#                     'question_id': question.id,
#                     'question_text': question.question_text,
#                     'question_type': question.question_type,
#                     'correct_answer': question.correct_answer,
#                     'correct_boolean': question.correct_boolean,
#                     'user_answer': user_answer,
#                     'correct': correct
#                 })
            
#             # Calculate time taken
#             time_taken = timezone.now() - session.start_time
            
#             # Save result
#             quiz_user = get_object_or_404(QuizUser, user=request.user)
#             result = QuizResult.objects.create(
#                 user=quiz_user,
#                 language=session.language,
#                 difficulty=session.difficulty,
#                 score=score,
#                 total_time=time_taken
#             )

#             # Delete session
#             session.delete()

#             # Redirect to result page
#             request.session['quiz_review'] = results
#             return redirect('quiz_result', result_id=result.id)
#     else:
#         form = QuizAnswerForm(questions)
    
#     return render(request, 'quiz_app/take_quiz.html', {
#         'form': form,
#         'questions': questions,
#         'session': session
#     })

@login_required
def take_quiz_view(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, user__user=request.user)
    question_ids = json.loads(session.questions)
    questions = list(Question.objects.filter(id__in=question_ids))
    total_questions = len(questions)

    # Track current question index in session
    current_index = request.session.get(f'quiz_{session_id}_current', 0)
    answers = request.session.get(f'quiz_{session_id}_answers', {})

    if request.method == 'POST':
        form = QuizAnswerForm([questions[current_index]], request.POST)
        if form.is_valid():
            field_name = f'question_{questions[current_index].id}'
            answers[str(questions[current_index].id)] = form.cleaned_data.get(field_name)
            request.session[f'quiz_{session_id}_answers'] = answers

            if 'next' in request.POST:
                current_index += 1
                request.session[f'quiz_{session_id}_current'] = current_index
                return redirect('take_quiz', session_id=session_id)
            elif 'submit' in request.POST:
                # Evaluate all answers
                score = 0
                results = []
                for idx, question in enumerate(questions):
                    user_answer = answers.get(str(question.id))
                    correct = False
                    score_increment = 0

                    if question.question_type == 'boolean':
                        if user_answer is not None and user_answer != '':
                            correct = (user_answer == str(question.correct_boolean))
                        else:
                            correct = False
                        if correct:
                            score_increment = 1

                    elif question.question_type == 'single_choice':
                        correct = user_answer == question.correct_answer
                        if correct:
                            score_increment = 1

                    elif question.question_type == 'multiple_choice':
                        if user_answer:
                            if isinstance(user_answer, str):
                                user_answer_set = set([user_answer])
                            else:
                                user_answer_set = set(user_answer)
                            correct_answer_set = set(ans.strip() for ans in question.correct_answer.split(',') if ans.strip())
                            correct = user_answer_set == correct_answer_set
                        else:
                            correct = False
                        if correct:
                            score_increment = 1

                    elif question.question_type == 'text':
                        if user_answer and question.correct_answer:
                            correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                            s1 = user_answer.strip().lower().split()
                            s2 = question.correct_answer.strip().lower().split()
                            words1 = set(s1)
                            words2 = set(s2)
                            matching_words = words1.intersection(words2)
                            score_increment = len(matching_words) / len(s2) if len(s2) > 0 else 0
                        else:
                            correct = False
                            score_increment = 0

                    score += score_increment
                    # print(score)

                    results.append({
                        'question_id': question.id,
                        'question_text': question.question_text,
                        'question_type': question.question_type,
                        'correct_answer': question.correct_answer,
                        'correct_boolean': question.correct_boolean,
                        'user_answer': user_answer,
                        'correct': correct
                    })
                # for idx, question in enumerate(questions):
                #     user_answer = answers.get(str(question.id))
                #     correct = False
                #     # ... (your existing answer checking logic here) ...
                #     if question.question_type == 'boolean':
                #         if user_answer is not None and user_answer != '':
                #             correct = (user_answer == str(question.correct_boolean))
                #         else:
                #             correct = False
                #     elif question.question_type == 'single_choice':
                #         correct = user_answer == question.correct_answer
                #     elif question.question_type == 'multiple_choice':
                #         if user_answer:
                #             if isinstance(user_answer, str):
                #                 user_answer_set = set([user_answer])
                #             else:
                #                 user_answer_set = set(user_answer)
                #             correct_answer_set = set(ans.strip() for ans in question.correct_answer.split(',') if ans.strip())
                #             correct = user_answer_set == correct_answer_set
                #         else:
                #             correct = False
                #     elif question.question_type == 'text':
                #         if user_answer and question.correct_answer:
                #             correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                #             s1= user_answer.strip().lower().split()
                #             s2= question.correct_answer.strip().lower().split()
                #             # Calculate score based on matching words
                #             words1 = set(s1)
                #             words2 = set(s2)
                #             matching_words = words1.intersection(words2)
                #             score += len(matching_words)/len(s2)
                #             print(score)
                #             # continue

                #         else:
                #             correct = False
                #     if correct and question.question_type != 'text':
                #         score += 1
                #     results.append({
                #         'question_id': question.id,
                #         'question_text': question.question_text,
                #         'question_type': question.question_type,
                #         'correct_answer': question.correct_answer,
                #         'correct_boolean': question.correct_boolean,
                #         'user_answer': user_answer,
                #         'correct': correct
                #     })
                time_taken = timezone.now() - session.start_time
                quiz_user = get_object_or_404(QuizUser, user=request.user)
                # print('Score=',score)
                result = QuizResult.objects.create(
                    user=quiz_user,
                    language=session.language,
                    difficulty=session.difficulty,
                    score=score,
                    total_time=time_taken
                )
                session.delete()
                request.session.pop(f'quiz_{session_id}_current', None)
                request.session.pop(f'quiz_{session_id}_answers', None)
                request.session['quiz_review'] = results
                return redirect('quiz_result', result_id=result.id)
    else:
        form = QuizAnswerForm([questions[current_index]])

    is_last = (current_index == total_questions - 1)
    return render(request, 'quiz_app/take_quiz.html', {
        'form': form,
        'question': questions[current_index],
        'current_index': current_index,
        'total_questions': total_questions,
        'is_last': is_last,
        'session': session
    })


@login_required
def quiz_result_view(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user__user=request.user)
    total_seconds = int(result.total_time.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    total = 10  # Total questions are 10
    # print(result.score)
    percentage = int((result.score / total) * 100)  # total is 10 in your context
    results = request.session.pop('quiz_review', [])
    attempted = sum(
    1 for item in results
    if item['user_answer'] not in [None, '', [], {}]
    )
    unattempted = len(results) - attempted
    # print(result.score)
    return render(request, 'quiz_app/quiz_result.html', {
        'score': result.score,
        'total': total,
        'results': results,
        'time_taken': result.total_time,
        'language': result.language,
        'difficulty': result.difficulty,
        'minutes': minutes,
        'seconds': seconds,
        'percentage': percentage,
        'attempted': attempted,
        'unattempted': unattempted,
    })


@login_required
def results_table_view(request):
    results = QuizResult.objects.all().order_by('-completed_at')
    return render(request, 'quiz_app/results_table.html', {'results': results})

@login_required
def results_data_view(request):
    results = QuizResult.objects.all().order_by('-completed_at')
    data = []
    # print(result.score)
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