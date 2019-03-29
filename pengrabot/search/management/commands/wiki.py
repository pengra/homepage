from django.core.management.base import BaseCommand, CommandError
from search.models import Result, Query
from django.db.utils import IntegrityError

import requests
import urllib.parse
import json

endpoint = "http://en.wikipedia.org/w/api.php?action=opensearch&limit=20&format=json&callback=portalOpensearchCallback&search="

class Command(BaseCommand):
    help = 'Wiki autocomplete a query and save results to the database.'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **kwargs):
        queries = kwargs['query']
        for query in queries.split("|"):
            query = query.strip().lower()
            print("wiki-ing", query)
            self.get_wiki(Query.objects.get_or_create(query=query)[0])

    def get_wiki(self, query):
        response = requests.get(endpoint + urllib.parse.quote(query.query))
        suggestions = json.loads(response.text[len('/**/portalOpensearchCallback('):-1])
        for i in range(20):
            title = suggestions[1][i]
            blurb = suggestions[2][i]
            url = suggestions[3][i]
            result = Result.objects.get_or_create(
                url=url,
            )[0]

            result = Result.objects.get(url=url)
            result.title = title
            result.blurb = blurb
            result.wiki = True
            result.save()

            query.results.add(result)
            


