from django.db import models

# Create your models here.
class Idea(models.Model):
	content  = models.CharField(max_length=1000) 
