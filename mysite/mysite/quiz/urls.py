from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('create_get/', views.create_get, name='create_get'),
    path('create_post/', views.create_post, name='create_post'),
    path('highscores/', views.highscores, name='highscores'),
    path('signup/', views.signup, name='signup'),
    path('questions/', views.questions, name='questions'),
]
