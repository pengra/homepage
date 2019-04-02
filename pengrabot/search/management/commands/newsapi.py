from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from search.models import Result, Query
import urllib.parse
import requests
import requests.exceptions
import time

key = "f0c77ef5220f4030a49263e579542244"


class Command(BaseCommand):
    help = 'Grab newsapi news articles'

    _endpoint = "https://newsapi.org/v2/everything?apiKey={key}&language=en&pageSize=50&q=".format(key=key)

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **kwargs):
        queries = kwargs['query'].split('|')
        for query in queries:
            query = query.lower().strip()
            print("Getting news:", query)
            query = Query.objects.get_or_create(query=query)[0]
            self.search(query)


    def search(self, query):
        response = requests.get(self._endpoint + urllib.parse.quote(query.query), headers={'User-Agent':'Pengrabot'})
        payload = response.json()
        articles = payload['articles']
        for article in articles:
            # source = article['source']
            # author = article['author']
            image_url = article['urlToImage']
            image = None
            
            title = article['title']
            blurb = article['description']
            if not blurb:
                blurb = "No Description"
            url = article['url']
            # published = article['publishedAt']
            result = Result.objects.get_or_create(
                url=url,
            )[0]
            
            print(title)
            
            result.title = title
            result.blurb = blurb
            result.news = True
            result.save()
            
            if image_url:
                try:
                    image = File(requests.get(image_url, stream=True).raw)
                    result.image.save(str(int(time.time())) + ".jpg", image)
                    result.save()
                except requests.exceptions.ConnectionError:
                    print("Error:", image_url)

            query.results.add(result)

            queries = [Query.objects.get_or_create(query=word)[0] for word in "".join([_ for _ in title.lower() if _.isalnum() or _.isspace()]).split(' ') if word]
            for q in queries:
                q.results.add(result)
