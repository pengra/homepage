from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from search.models import Result, Query

import urllib.parse

import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = "Conduct a DuckDuckGo search"

    _endpoint = "https://duckduckgo.com/html/?q="
    
    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **kwargs):
        queries = kwargs['query'].split('|')
        for query in queries:
            query = query.lower().strip()
            print("DuckDuckGo-ing", query)
            query, created = Query.objects.get_or_create(query=query)
            self.search(query)
            

    def search(self, query):
        response = requests.get(self._endpoint + urllib.parse.quote(query.query), headers={'User-Agent':'Pengrabot'})
        soup = BeautifulSoup(response.text)
        results = soup.find('div', id='links').find_all('div', **{'class': 'result'})
        print('=' * 80)
        for result in results:
            try:
                title = result.find('h2', **{'class': 'result__title'}).text.strip()
            except AttributeError:
                title = 'Title N/A'
            try:
                url = urllib.parse.unquote(result.find('a', **{'class': 'result__a'})['href'][len('/l/?kh=-1&uddg='):])
                netloc = urllib.parse.urlparse(url).netloc
            except AttributeError:
                continue
            try:
                snippet = result.find('a', **{'class': 'result__snippet'}).get_text(separator=" ", strip=True)
            except AttributeError:
                snippet = "No snippet available"
            result, created = Result.objects.get_or_create(
                url=url,
            )
            if created:
                result.title = title
                result.blurb = snippet
            result.duckduckgo = True
            result.wiki = 'wikipedia.org' in netloc
            result.arxiv = 'arxiv.org' in netloc
            result.uw = 'uw.edu' in netloc or 'washington.edu' in netloc
            result.edu = (
                '.edu' in netloc or 
                'khanacademy.org' in netloc or 
                'brilliant.org' in netloc or
                'unacademy.org' in netloc or
                'udemy.com' in netloc
            )
            result.save()
            query.results.add(result)
            query.save()
            print(title)
            print(url)
            print(snippet)
            print('=' * 80)


        