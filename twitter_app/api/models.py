from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    term = models.CharField(max_length=50)
    lang = models.CharField(max_length=2)
    country = models.CharField(max_length=50)
    referenced_tweets = models.BooleanField()
    place = models.BooleanField()
    source = models.BooleanField()
    num_tw = models.PositiveSmallIntegerField(MinValueValidator(10))
    priority = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000), MinValueValidator(1)])

    create_at = models.DateTimeField(auto_now_add=True)
