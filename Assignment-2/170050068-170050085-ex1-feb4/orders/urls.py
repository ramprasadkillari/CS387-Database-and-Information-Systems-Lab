from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('login/',views.Login),
	path('orders',views.user_direct)
]