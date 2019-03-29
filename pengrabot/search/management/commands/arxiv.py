from django.core.management.base import BaseCommand, CommandError

import feedparser

from search.models import Result, Query
import urllib.parse
import requests

class Command(BaseCommand):
    help = 'Grab arxiv articles'

    _endpoint = "http://export.arxiv.org/api/query?start=0&max_results=50&search_query=all:"

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **kwargs):
        queries = kwargs['query'].split('|')
        for query in queries:
            query = query.lower().strip()
            print("Getting academic articles:", query)
            query = Query.objects.get_or_create(query=query)[0]
            self.search(query)


    def search(self, query):
        feed = feedparser.parse(self._endpoint + urllib.parse.quote(query.query))
        for entry in feed.entries:
            url = entry.id
            title = entry.title
            blurb = entry.summary

            result = Result.objects.get_or_create(
                url=url
            )[0]
            result.title = title
            result.blurb = blurb
            result.arxiv = True
            result.save()
            query.results.add(result)
            

