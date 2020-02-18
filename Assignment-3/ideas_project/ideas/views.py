from django.shortcuts import render
# Create your views here.
from .models import Idea
from rest_framework import viewsets
from ideas.serializers import IdeaSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer

def home(request):
    # if request.user.is_authenticated:
    return render(request, 'ideas.html')
