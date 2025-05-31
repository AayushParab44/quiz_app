from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

from . import views



from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quiz/select/', views.quiz_selection_view, name='quiz_selection'),
    path('quiz/take/<int:session_id>/', views.take_quiz_view, name='take_quiz'),
    path('results/', views.results_table_view, name='results_table'),
    path('results/data/', views.results_data_view, name='results_data'),
    path('quiz/result/<int:result_id>/', views.quiz_result_view, name='quiz_result'),
]

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('quiz_app.urls')),
# ]



# urlpatterns = [
#     path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('register/', views.register_view, name='register'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('quiz/select/', views.quiz_selection_view, name='quiz_selection'),
#     path('quiz/take/<int:session_id>/', views.take_quiz_view, name='take_quiz'),
#     path('results/', views.results_table_view, name='results_table'),
#     path('results/data/', views.results_data_view, name='results_data'),
#     path('quiz/result/<int:result_id>/', views.quiz_result_view, name='quiz_result'),
# ]

# urlpatterns = [
#     path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
#     path('', views.home, name='home'),  # Example home view
#     # Authentication URLs

#     path('', auth_views.LoginView.as_view(), name='login'),
#     path('register/', views.register_view, name='register'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
#     # Quiz URLs
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('quiz/select/', views.quiz_selection_view, name='quiz_selection'),
#     path('quiz/take/<int:session_id>/', views.take_quiz_view, name='take_quiz'),
#     path('results/', views.results_table_view, name='results_table'),
#     path('results/data/', views.results_data_view, name='results_data'),
# ]
