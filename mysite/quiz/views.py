import datetime
import requests
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View

#Imports the appropriate models.
from .models import Tournament, Question, Answer, HighScore

#Checks if the user is a super user.
can_create = user_passes_test(lambda u: u.is_superuser)
# user: admin
# pass: admin123


class SignUpView(View):
    def post(self, request):
        #Gets user information from form and creates a user.
        user = User.objects.create_user(first_name=request.POST.get('firstname')
                                        , last_name=request.POST.get('lastname')
                                        , email=request.POST.get('email')
                                        , username=request.POST.get('username')
                                        , password=request.POST.get('password'))
        #Saves the created user to the database.
        user.save()
        #Sends user to the login view.
        return render(request, 'quiz/login.html')

    def get(self, request):
        #Sends user to the sign up view.
        return render(request, 'quiz/signup.html')


class LoginView(View):
    def post(self, request):
        #Gets the username and password from the login form.
        username = request.POST['username']
        password = request.POST['password']
        #Checks the information entered matches an actual user.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #If user is information is valid logs the user in.
            login(request, user)
        #Sends the user to the home screen.
        return HttpResponseRedirect(reverse('quiz:home'))

    def get(self, request):
        #Sends the user to the login screen.
        return render(request, 'quiz/login.html')


class LogoutView(View):
    #Requires the user to be logged in.
    @method_decorator(login_required)
    def get(self, request):
        #Logs the user out.
        logout(request)
        #Sends the user to the login screen.
        return render(request, 'quiz/login.html')


class HomeView(View):
    #Requires the user to be logged in.
    @method_decorator(login_required)
    def get(self, request):
        #Gets a list of active tournaments
        active_tournaments = Tournament.objects.filter(start_date__lte=datetime.date.today(), end_date__gt=datetime.date.today())
        #Gets a list of upcoming tournaments
        upcoming_tournaments = Tournament.objects.filter(start_date__gt=datetime.date.today())
        #Creates the args dictionary to pass in the render.
        args = {'active': active_tournaments, 'upcoming': upcoming_tournaments}
        #Sends the user to the home screen.
        return render(request, 'quiz/home.html', args)


class CreateTournamentView(View):
    #Requires the user to be logged in as a super user.
    @method_decorator(can_create)
    def get(self, request):
        #Creates a response to get the catergories from the api.
        response = requests.get('https://opentdb.com/api_category.php')
        #Turns the response into json.
        data = response.json()
        categories = {}
        #Populates the categories dictionary with results from the json.
        for i in data['trivia_categories']:
            categories.update({i['id']: i['name']})
        #Sends the user to the create screen.
        return render(request, 'quiz/create.html', {'categories': categories})

    # Requires the user to be logged in as a super user.
    @method_decorator(can_create)
    def post(self, request):
        #Creates the start of the api string.
        api = 'https://opentdb.com/api.php?amount=10'
        #Checks if the category is not set to any.
        if request.POST.get('category') != 'Any':
            #Adds the api for category if a category was selected.
            api = api + '&category=%s' % (request.POST.get('category'))
        # Checks if the difficulty is not set to any.
        if request.POST.get('difficulty') != 'Any':
            # Adds the api for category if a difficulty was selected.
            api = api + '&difficulty = % s' % (request.POST.get('difficulty').lower())
        #Creates a response to get the questions from the api.
        response = requests.get(api)
        #Turns the response into json.
        data = response.json()
        #Checks if the api returned any questions.
        if data['response_code'] == 0:
            #Creates a tournament with the user information from the form.
            tournament = Tournament.objects.create(name=request.POST.get('name')
                                                   , start_date=request.POST.get('start_date')
                                                   , end_date=request.POST.get('end_date')
                                                   , category=request.POST.get('category')
                                                   , difficulty=request.POST.get('difficulty'))
            #Saves the tournament to the database.
            tournament.save()
            #Loops through the received questions.
            for r in data['results']:
                #Creates the question objects using the tournament.
                question = Question.objects.create(tournament=tournament
                                                   , question_text=r['question']
                                                   , correct_answer=r['correct_answer'])
                #Saves the questions to the database.
                question.save()
                #Adds the correct answer object to the answers for each question using the question id.
                answer = Answer.objects.create(question=question, incorrect_answer=r['correct_answer'])
                #Saves the answer to the database.
                answer.save()
                #Loops through the incorrect answers.
                for a in r['incorrect_answers']:
                    #Adds the incorrect answers for the question using the question id.
                    answer = Answer.objects.create(question=question, incorrect_answer=a)
                    #Saves the answers to the database.
                    answer.save()
        #Sends the user to the homepage.
        return HttpResponseRedirect(reverse('quiz:home'))


class TournamentView(View):
    # Requires the user to be logged in.
    @method_decorator(login_required)
    def get(self, request, tournament_id):
        #Gets the tournament from the database based on the tournament id.
        tournament = Tournament.objects.get(id=tournament_id)
        #Checks to see if the user already has highscore data for this torunament
        try:
            highscore = HighScore.objects.get(username=request.user.username, tournament_id=tournament_id)
        #If the user does not have highscore data already it creates it.
        except ObjectDoesNotExist:
            highscore = HighScore.objects.create(username=request.user.username,
                                                 tournament_id=tournament_id,
                                                 current_score=0,
                                                 current_question=0)
            #Saves the highscore data to the database.
            highscore.save()

        #Checks if the users current question for this tournament is less than 10.
        if highscore.current_question < 10:
            #Gets the questions for the tournament based on the tournament id.
            questions = Question.objects.filter(tournament=tournament_id).order_by('id')
            #Gets the current question.
            question = questions[highscore.current_question]
            #Gets the answers for the current question.
            answers = Answer.objects.filter(question=question)
            #Creates the arguments to pass into the tournament screen.
            args = {'tournament_id': tournament_id, 'tournament_name': tournament.name,
                    'question_number': highscore.current_question + 1, 'question': question, 'answers': answers}
            #Sends the user to the tournament screen.
            return render(request, 'quiz/tournament.html', args)
        #If user already is already finished the tournament
        else:
            #Sends the user to the results screen with their score.
            return HttpResponseRedirect(reverse('quiz:results', kwargs={'score': highscore.current_score}))

    def post(self, request, tournament_id):
        #Gets the tournament using the tournament id.
        tournament = Tournament.objects.get(id=tournament_id)
        #Gets the answer the user entered.
        user_answer = request.POST.get('answers')

        #Gets the users highscore data for the current tournament.
        highscore = HighScore.objects.get(username=request.user.username, tournament_id=tournament.id)
        questions = Question.objects.filter(tournament=tournament.id).order_by('id')
        question = questions[highscore.current_question]

        #Checks if the answer entered by the user is the same as the correct answer from the database.
        if user_answer == question.correct_answer:
            #Increments the users score by one.
            highscore.current_score += 1
            #Sends a message to the user they got the answer correct.
            messages.success(request, 'Woohoo! Last question was correct!')
        #Checks if the users answer was wrong.
        elif user_answer != question.correct_answer:
            #Sends a message to the user that the answer they provided was incorrect.
            messages.error(request, 'Uhoh! Last question was incorrect!')

        #Increments the users highscore current question data by one.
        highscore.current_question += 1
        #Saves the highscore data to the database.
        highscore.save()
        #Sends the user to the next question.
        return HttpResponseRedirect(reverse('quiz:tournament', kwargs={'tournament_id': tournament.id}))


class HighScoresView(View):
    # Requires the user to be logged in.
    @method_decorator(login_required)
    def get(self, request):
        #Creates an empty list of highscore data
        highscores = []
        #Gets the tournament information from the database.
        tournaments = Tournament.objects.all()

        #Goes through each of the tournaments.
        for t in tournaments:
            #Gets all of the highscore for a given tournament ordered by current score descending.
            h = HighScore.objects.filter(tournament_id=t.id, current_question=10).order_by('-current_score')
            #checks if there is highscore data for that tournament.
            if len(h) > 0:
                #Adds that highscore entry to the highscores list.
                highscores.append(h[0])

        #Creates the arguments and sends the user to highscores screen.
        args = {'highscores': highscores, 'tournaments': tournaments}
        return render(request, 'quiz/highscores.html', args)


class Results(View):
    # Requires the user to be logged in.
    @method_decorator(login_required)
    def get(self, request, score):
        #Puts the passed in score in to args and sends them to the results screen.
        args = {'score': score}
        return render(request, 'quiz/results.html', args)

