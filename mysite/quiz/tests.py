from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import TestCase


class SignUpTestCase(TestCase):
    def test_post(self):
        args = {'firstname': 'homer', 'lastname': 'simpson', 'email': 'homersimpson@gmail.com', 'username': 'homer1', 'password': 'margeSimpson'}
        response = self.client.post('/quiz/signup/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/login.html')

    def test_get(self):
        response = self.client.get('/quiz/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/signup.html')

class LoginTestCase(TestCase):
    def test_post(self):
        User.objects.create_user(username='homer', password='margeSimpson')
        args = {'username': 'homer', 'password': 'margeSimpson'}
        response = self.client.post('/quiz/login/', args, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/home.html')

    def test_get(self):
        response = self.client.get('/quiz/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/login.html')

class LogoutTestCase(TestCase):
    def test_get(self):
        User.objects.create_user(username='homer', password='margeSimpson')
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/logout/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/login.html')

class HomeTestCase(TestCase):
    def test_get(self):
        response = self.client.get('/quiz/home/')
        self.assertEqual(response.status_code, 302)

        User.objects.create_user(username='homer', password='margeSimpson')
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/home.html')

class CreateTestCase(TestCase):
    def test_get(self):
        response = self.client.get('/quiz/create/')
        self.assertEqual(response.status_code, 302)

    def test_get_user(self):
        User.objects.create_user(username='homer', password='margeSimpson')
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/create/')
        self.assertEqual(response.status_code, 302)

    def test_get_superuser(self):
        User.objects.create_superuser(username='homer', password='margeSimpson', email="homerSimpson@gmail.com")
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/create/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/create.html')

#class TournamentTestCase(TestCase):
    #def test_get(self):

class HighScoresTestCase(TestCase):
    def test_get(self):
        User.objects.create_user(username='homer', password='margeSimpson')
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/highscores/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/highscores.html')

class ResultsTestCase(TestCase):
    def test_get(self):
        User.objects.create_user(username='homer', password='margeSimpson')
        login_response = self.client.login(username='homer', password='margeSimpson')
        self.assertTrue(login_response)
        response = self.client.get('/quiz/results/10')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/results.html')