from django.urls import include, path
from gh_auth import views
urlpatterns = [

    path('ghauthenticated/',views.github_authenticated),
    path('ghlogin/',views.ghlogin),
]