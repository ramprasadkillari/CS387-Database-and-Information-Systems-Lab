from django.contrib import admin
from forum.models import Topic, Comment, User
# Register your models here.
from django.contrib import admin
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(User)
