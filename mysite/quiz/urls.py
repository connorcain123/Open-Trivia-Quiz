from django.urls import path

from quiz.views import CreateTournamentView, LogoutView, HomeView, LoginView, SignUpView, HighScoresView, \
    TournamentView, Results
from . import views

app_name = 'quiz'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', CreateTournamentView.as_view(), name='create'),
    path('highscores/', HighScoresView.as_view(), name='highscores'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('tournament/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('checkAnswer/<int:tournament_id>/', TournamentView.as_view(), name='checkanswer'),
    path('results/<int:score>', Results.as_view(), name='results')
]
