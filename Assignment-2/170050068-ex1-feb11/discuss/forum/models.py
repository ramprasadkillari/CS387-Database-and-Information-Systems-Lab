from django.db import models

# Create your models here.


class User(models.Model):
     name =  models.CharField(max_length=30, blank=True)   # possible to have name clashes. 

class Topic(models.Model):
     title = models.CharField(max_length=200, blank=False,null=False)
     created_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
     created_on = models.DateTimeField(auto_now_add=True)

class Comment(models.Model): 
     topic = models.ForeignKey(Topic,null=True,on_delete=models.SET_NULL)
     created_by = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
     subject = models.CharField(max_length=200, blank=False)     # must not be empty
     message = models.CharField(max_length=200, blank=False) 
