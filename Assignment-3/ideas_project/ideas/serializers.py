from .models import Idea
from rest_framework import serializers


class IdeaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Idea
        fields = ['content']
