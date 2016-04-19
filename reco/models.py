from __future__ import unicode_literals

from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here
class UserProfile(models.Model):
	user=models.OneToOneField(User, blank=False, unique=True)
	age=models.CharField(max_length=3)
	SEXES=(
			('Male','Male'),
			('Female','Female'),
			('Other','Other'),
			)
	sex=models.CharField(max_length=1, choices=SEXES)


class Activities(models.Model):
	TYPES=(
			('FD','Food'),
			('TR','Tour'),
			('MV','Movie'),
			('OT','Other')
			)
	actype=models.CharField(max_length=1, choices=TYPES)
	name=models.CharField(max_length=100)
	detail=models.CharField(max_length=300)

class Rating(models.Model):
	user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	activity=models.ForeignKey(Activities, on_delete=models.CASCADE)
	rating=models.IntegerField(default=5)

