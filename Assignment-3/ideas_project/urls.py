"""ideas_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from ideas import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'ideas', views.IdeaViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('home/',views.home1),
    path('',views.home,name="home"),
    path('',include('gh_auth.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls), path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    ]