from rest_framework import serializers
from search.models import Result

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = (
            'id',
            'clicks',
            'url',
            'title',
            'blurb',
            'grabbed',
            'personal',
            'news',
            'hackernews',
            'uw',
            'wiki',
            'arxiv',
            'duckduckgo',
            'image',
            'chan',
            'sx',
        )