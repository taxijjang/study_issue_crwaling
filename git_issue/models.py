from django.db import models

# Create your models here.
class Issue(models.Model):
    issue = models.CharField(max_length=100)

    def __str__(self):
        return self.issue

class Question(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    question_link = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class Customer(models.Model):
    issue = models.ForeignKey(Issue, on_delete = models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Solve(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    problem_solve = models.CharField(max_length=200)

    def __str__(self):
        return self.problem_solve