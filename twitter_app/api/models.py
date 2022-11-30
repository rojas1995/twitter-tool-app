from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    term = models.CharField(max_length=512)
    lang = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    referenced_tweets = models.BooleanField()
    place = models.BooleanField()
    source = models.BooleanField()
    num_tw = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000), MinValueValidator(1)])
    priority = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])  # 1 higher, 5 lower priority

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['priority', 'create_at']




class JobLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    job_id = models.PositiveSmallIntegerField()
    term = models.CharField(max_length=512)
    lang = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    referenced_tweets = models.BooleanField()
    place = models.BooleanField()
    source = models.BooleanField()
    num_tw = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000), MinValueValidator(1)])
    priority = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)])  # 1 higher, 5 lower priority

    create_at = models.DateTimeField(null=True)
    execution_time = models.DateTimeField(auto_now_add=True)
    execution_success = models.BooleanField()

    class Meta:
        ordering = ['execution_time']
