from django.shortcuts import render
# Create your views here.
from .models import Idea
from rest_framework import viewsets
from ideas.serializers import IdeaSerializer
from django.contrib.auth.decorators import login_required


class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

def home1(request):
    # if request.user.is_authenticated:
    return render(request, 'ideas.html')

# Create your views here.
def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')