from rest_framework import serializers
from search.models import Result, Query

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = (
            'id',
            'query',
            'result_count'
        )
    
    result_count = serializers.IntegerField(source='results_count')

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
            'queries',
        )

    queries = serializers.StringRelatedField(source='filtered_queries', many=True)