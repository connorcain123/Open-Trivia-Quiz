from django.db import models


class Tournament(models.Model):

    name = models.CharField(
        max_length=15,
        default='Tournament Name'
    )

    start_date = models.DateField()

    end_date = models.DateField()

    category = models.CharField(
        max_length=15,
        default='Any'
    )

    difficulty = models.CharField(
        max_length=10,
        default='Any'
    )


class Question(models.Model):

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE
    )
    question_text = models.CharField(
        max_length=255
    )
    correct_answer = models.CharField(
        max_length=100
    )


class Answer(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    incorrect_answer = models.CharField(
        max_length=100
    )


class HighScore(models.Model):

    username = models.CharField(
        max_length=100
    )
    tournament_id = models.IntegerField()
    current_score = models.IntegerField()
    current_question = models.IntegerField()
