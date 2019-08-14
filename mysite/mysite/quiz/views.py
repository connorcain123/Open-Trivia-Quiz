import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Tournament, Question, Answer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    return render(request, 'quiz/login.html')


def home(request):
    username = 'Connor'

    active_tournaments = Tournament.objects.all()
    #upcoming_tournaments =
    args = {'active': active_tournaments, 'username': username}
    return render(request, 'quiz/home.html', args)


def create_post(request):
    tournament = Tournament.objects.create(name=request.POST.get('name')
                                           , start_date=request.POST.get('start_date')
                                           , end_date=request.POST.get('end_date')
                                           , category=request.POST.get('category')
                                           , difficulty=request.POST.get('difficulty'))
    tournament.save()

    response = requests.get('https://opentdb.com/api.php?amount=10&category=%s&difficulty=%s' % (tournament.category, tournament.difficulty.lower()))
    data = response.json()
    for r in data['results']:
        question = Question.objects.create(tournament=tournament
                                           , question_text=r['question']
                                           , correct_answer=r['correct_answer'])
        question.save()
        for a in r['incorrect_answers']:
            answer = Answer.objects.create(question=question, incorrect_answer=a)
            answer.save()

    return HttpResponseRedirect(reverse('quiz:home'))


def create_get(request):
    response = requests.get('https://opentdb.com/api_category.php')
    data = response.json()
    categories = {}
    for i in data['trivia_categories']:
        categories.update({i['id']: i['name']})
    return render(request, 'quiz/create.html',{'categories': categories})


def questions(request):
    questions = Question.objects.all()
    answers = Answer.objects.all()
    args = {'questions': questions, 'answers': answers}
    return render(request, 'quiz/tournament.html', args)


def highscores(request):
    list = [23,4,2,4,5,3,5]
    args = {'list': list}
    return render(request, 'quiz/highscores.html', args)


def signup(request):
    return render(request, 'quiz/signup.html')
